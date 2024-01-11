import os
import numpy as np
from PIL import Image
import tifffile as tf
from reportlab.pdfgen import canvas

def redimensionar_pagina(pagina, nova_largura):
    largura_original = pagina.shape[1]
    fator_redimensionamento = nova_largura / largura_original
    nova_altura = int(pagina.shape[0] * fator_redimensionamento)
    return np.array(Image.fromarray(pagina).resize((nova_largura, nova_altura)))

def converter_bw_separar_unir(input_path, output_path):
    # Verifica se o diretório de saída existe, se não, cria
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Lista todos os arquivos de imagem no diretório de entrada
    imagens = [file for file in os.listdir(input_path) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.tif'))]

    nova_largura = 2496  # Largura desejada para redimensionamento

    for imagem_nome in imagens:
        # Caminho completo para a imagem
        imagem_path = os.path.join(input_path, imagem_nome)

        # Abre a imagem usando Pillow
        imagem_pillow = Image.open(imagem_path)

        # Passo 4: Separa imagens com mais de uma página
        if imagem_pillow.n_frames > 1:
            paginas_separadas = []

            for idx in range(imagem_pillow.n_frames):
                # Seleciona a página
                imagem_pillow.seek(idx)

                # Converte a página para escala de cinza
                pagina_bw = np.array(imagem_pillow.convert("L"))

                # Adiciona a página à lista
                paginas_separadas.append(pagina_bw)

                # Salva a imagem tratada no diretório de saída
                nome_arquivo_separado = f"{os.path.splitext(imagem_nome)[0]}_{idx + 1}_separado.tif"
                caminho_saida_separado = os.path.join(output_path, nome_arquivo_separado)
                tf.imwrite(caminho_saida_separado, pagina_bw)

            # Passo 7: Junta as páginas separadas novamente
            imagem_concatenada = np.concatenate(paginas_separadas, axis=0)

            # Salva a imagem concatenada como TIFF
            nome_arquivo_unido = f"{os.path.splitext(imagem_nome)[0]}_unido.tif"
            caminho_saida_unido = os.path.join(output_path, nome_arquivo_unido)
            tf.imwrite(caminho_saida_unido, imagem_concatenada)
        else:
            # Passo 5: Converte a imagem para preto e branco
            imagem_bw = np.array(imagem_pillow.convert("L"))

            # Salva a imagem tratada como TIFF
            nome_arquivo_tratado = f"{os.path.splitext(imagem_nome)[0]}_tratado.tif"
            caminho_saida_tratado = os.path.join(output_path, nome_arquivo_tratado)
            tf.imwrite(caminho_saida_tratado, imagem_bw)

if __name__ == "__main__":
    # Diretório de entrada e saída
    diretorio_entrada = "Caminho\\para\\diretorio_X"
    diretorio_saida = "Caminho\\para\\diretorio_Y"

    converter_bw_separar_unir(diretorio_entrada, diretorio_saida)
