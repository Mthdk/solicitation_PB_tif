import os
from PIL import Image, TiffImagePlugin

def converter_bw_concatenar(input_path, output_path):
    # Verifica se o diretório de saída existe, se não, cria
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Lista todos os arquivos .tif ou .tiff no diretório de entrada
    imagens = [file for file in os.listdir(input_path) if file.lower().endswith(('.tif', '.tiff'))]

    imagens_concatenadas = []  # Lista para armazenar imagens de cada página

    for imagem_nome in imagens:
        # Caminho completo para a imagem
        imagem_path = os.path.join(input_path, imagem_nome)

        # Abre a imagem TIFF usando Pillow
        imagem_tiff = Image.open(imagem_path)

        for idx in range(imagem_tiff.n_frames):
            # Seleciona a página
            imagem_tiff.seek(idx)

            # Converte a página para escala de cinza
            pagina_bw = imagem_tiff.convert("L")

            # Adiciona a página à lista
            imagens_concatenadas.append(pagina_bw)

    # Salva as imagens concatenadas como páginas em um único arquivo TIFF
    nome_arquivo_concatenado = "concatenado.tif"
    caminho_saida_concatenado = os.path.join(output_path, nome_arquivo_concatenado)

    # Cria um novo arquivo TIFF
    with TiffImagePlugin.AppendingTiffWriter(caminho_saida_concatenado, True) as tf:
        for imagem in imagens_concatenadas:
            # Adiciona cada página como um quadro ao arquivo TIFF
            tf.write(imagem)

if __name__ == "__main__":
    # Diretório de entrada e saída
    diretorio_entrada = "Caminho\\para\\diretorio_X"
    diretorio_saida = "Caminho\\para\\diretorio_Y"

    converter_bw_concatenar(diretorio_entrada, diretorio_saida)
