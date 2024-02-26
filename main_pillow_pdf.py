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

    # Lista todos os arquivos .tif ou .tiff no diretório de entrada
    imagens = [file for file in os.listdir(input_path) if file.lower().endswith(('.tif', '.tiff'))]

    nova_largura = 2496  # Largura desejada para redimensionamento

    imagens_tratadas = []  # Lista para armazenar imagens de cada página

    for imagem_nome in imagens:
        # Caminho completo para a imagem
        imagem_path = os.path.join(input_path, imagem_nome)

        # Abre a imagem TIFF usando Pillow
        imagem_tiff = Image.open(imagem_path)

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

    # União das páginas em um único arquivo PDF
    nome_arquivo_unido = "unido.pdf"
    caminho_saida_unido = os.path.join(output_path, nome_arquivo_unido)

    # Criando o arquivo PDF
    with open(caminho_saida_unido, 'wb') as pdf_file:
        c = canvas.Canvas(pdf_file)

        for imagem in imagens_tratadas:
            # Adiciona a imagem ao PDF
            img_data = Image.fromarray(imagem).tobytes("raw", "L")
            c.drawImage(img_data, 0, 0, width=nova_largura, height=imagem.shape[0])

            # Adiciona uma nova página ao PDF
            c.showPage()

        c.save()

def unir_imagens(input_path):
    imagens = [file for file in os.listdir(input_path) if file.lower().endswith('_tratada.tif')]
    imagens_a_unir = {}

    # Encontrando imagens a serem unidas
    for imagem_nome in imagens:
        nome_base = "_".join(imagem_nome.split("_")[:-3])  # Obtém o nome base antes do sufixo "_pagina_x_tratada"
        if nome_base not in imagens_a_unir:
            imagens_a_unir[nome_base] = [imagem_nome]
        else:
            imagens_a_unir[nome_base].append(imagem_nome)

    # Unindo imagens e renomeando
    for nome_base, imagens_lista in imagens_a_unir.items():
        if len(imagens_lista) > 1:
            imagens_unidas = [np.array(Image.open(os.path.join(input_path, imagem))) for imagem in imagens_lista]
            imagem_concatenada = np.concatenate(imagens_unidas, axis=0)
            caminho_saida_unido = os.path.join(input_path, f"{nome_base}_unido.tif")
            tf.imwrite(caminho_saida_unido, imagem_concatenada)

            # Removendo imagens antigas
            for imagem in imagens_lista:
                os.remove(os.path.join(input_path, imagem))

if __name__ == "__main__":
    # Diretório de entrada e saída
    diretorio_entrada = "Caminho\\para\\diretorio_X"
    diretorio_saida = "Caminho\\para\\diretorio_Y"

    converter_bw_separar_unir(diretorio_entrada, diretorio_saida)
    unir_imagens(diretorio_saida)
