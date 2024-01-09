import os
from PIL import Image, TiffImagePlugin

def converter_bw_concatenar(input_path, output_path):
    # Verifica se o diretório de saída existe, se não, cria
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Lista todos os arquivos .tif ou .tiff no diretório de entrada
    imagens = [file for file in os.listdir(input_path) if file.lower().endswith(('.tif', '.tiff'))]

    imagens_concatenadas = []  # Lista para armazenar caminhos das imagens de cada página

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

            # Salva a página como um arquivo temporário
            caminho_pagina_temporario = os.path.join(output_path, f"temp_pagina_{len(imagens_concatenadas)}.tif")
            pagina_bw.save(caminho_pagina_temporario, format='TIFF')

            # Adiciona o caminho da página à lista
            imagens_concatenadas.append(caminho_pagina_temporario)

    # Cria um único arquivo TIFF combinando todas as páginas
    nome_arquivo_concatenado = "concatenado.tif"
    caminho_saida_concatenado = os.path.join(output_path, nome_arquivo_concatenado)

    with TiffImagePlugin.AppendingTiffWriter(caminho_saida_concatenado, True) as tf:
        for caminho_pagina in imagens_concatenadas:
            # Lê o arquivo temporário e adiciona como um quadro ao arquivo TIFF
            with open(caminho_pagina, 'rb') as pagina_temporario:
                tf.write(pagina_temporario.read())

            # Remove o arquivo temporário após adicionar ao TIFF
            os.remove(caminho_pagina)

if __name__ == "__main__":
    # Diretório de entrada e saída
    diretorio_entrada = "Caminho\\para\\diretorio_X"
    diretorio_saida = "Caminho\\para\\diretorio_Y"

    converter_bw_concatenar(diretorio_entrada, diretorio_saida)
