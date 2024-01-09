import os
from PIL import Image

def converter_bw_concatenar(input_path, output_path):
    # Verifica se o diretório de saída existe, se não, cria
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Lista todos os arquivos .tif ou .tiff no diretório de entrada
    imagens = [file for file in os.listdir(input_path) if file.lower().endswith(('.tif', '.tiff'))]

    for imagem_nome in imagens:
        # Caminho completo para a imagem
        imagem_path = os.path.join(input_path, imagem_nome)

        # Abre a imagem TIFF usando Pillow
        imagem_tiff = Image.open(imagem_path)

        imagens_concatenadas = []  # Lista para armazenar imagens de cada página

        for idx in range(imagem_tiff.n_frames):
            # Seleciona a página
            imagem_tiff.seek(idx)

            # Converte a página para escala de cinza
            pagina_bw = imagem_tiff.convert("L")

            # Adiciona a página à lista
            imagens_concatenadas.append(pagina_bw)

        # Concatena as imagens verticalmente
        imagem_concatenada = Image.new("L", (imagens_concatenadas[0].width, sum(imagem.height for imagem in imagens_concatenadas)))
        offset = 0
        for imagem in imagens_concatenadas:
            imagem_concatenada.paste(imagem, (0, offset))
            offset += imagem.height

        # Salva a imagem concatenada no diretório de saída
        nome_arquivo_concatenado = f"{os.path.splitext(imagem_nome)[0]}_concatenado.png"
        caminho_saida_concatenado = os.path.join(output_path, nome_arquivo_concatenado)
        imagem_concatenada.save(caminho_saida_concatenado)

if __name__ == "__main__":
    # Diretório de entrada e saída
    diretorio_entrada = "Caminho\\para\\diretorio_X"
    diretorio_saida = "Caminho\\para\\diretorio_Y"

    converter_bw_concatenar(diretorio_entrada, diretorio_saida)
