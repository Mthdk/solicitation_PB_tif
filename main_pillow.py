import os
import numpy as np
from PIL import Image
import tifffile as tf

def redimensionar_pagina(pagina, nova_largura):
    largura_original = pagina.shape[1]
    fator_redimensionamento = nova_largura / largura_original
    nova_altura = int(pagina.shape[0] * fator_redimensionamento)
    return np.array(Image.fromarray(pagina).resize((nova_largura, nova_altura)))

def converter_bw_separar(input_path, output_path):
    # Verifica se o diretório de saída existe, se não, cria
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Lista todos os arquivos .tif ou .tiff no diretório de entrada
    imagens = [file for file in os.listdir(input_path) if file.lower().endswith(('.tif', '.tiff'))]

    nova_largura = 2496  # Largura desejada para redimensionamento

    for imagem_nome in imagens:
        # Caminho completo para a imagem
        imagem_path = os.path.join(input_path, imagem_nome)

        # Abre a imagem TIFF usando Pillow
        imagem_tiff = Image.open(imagem_path)

        imagens_tratadas = []  # Lista para armazenar imagens de cada página

        for idx in range(imagem_tiff.n_frames):
            # Seleciona a página
            imagem_tiff.seek(idx)

            # Converte a página para escala de cinza
            pagina_bw = np.array(imagem_tiff.convert("L"))

            # Redimensiona a página para ter a mesma largura
            pagina_redimensionada = redimensionar_pagina(pagina_bw, nova_largura)

            # Adiciona a página à lista
            imagens_tratadas.append(pagina_redimensionada)

            # Salva a imagem tratada no diretório de saída
            nome_arquivo_tratado = f"{os.path.splitext(imagem_nome)[0]}_pagina_{idx + 1}_tratada.tif"
            caminho_saida_tratado = os.path.join(output_path, nome_arquivo_tratado)
            tf.imwrite(caminho_saida_tratado, pagina_redimensionada)

if __name__ == "__main__":
    # Diretório de entrada e saída
    diretorio_entrada = "Caminho\\para\\diretorio_X"
    diretorio_saida = "Caminho\\para\\diretorio_Y"

    converter_bw_separar(diretorio_entrada, diretorio_saida)
