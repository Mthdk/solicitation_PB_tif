from PIL import Image
import os
import pytesseract

def converte_para_pb(diretorio_origem, diretorio_destino):
    # Altera o diretório de trabalho para o diretório do script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Certifica-se de que o diretório de destino existe
    if not os.path.exists(diretorio_destino):
        os.makedirs(diretorio_destino)

    # Lista todos os arquivos no diretório de origem
    arquivos = os.listdir(diretorio_origem)

    for arquivo in arquivos:
        caminho_arquivo = os.path.join(diretorio_origem, arquivo)

        # Verifica se é um arquivo do tipo tif
        if arquivo.lower().endswith(".tif"):
            # Abre a imagem TIFF
            imagem_tif = Image.open(caminho_arquivo)

            # Obtém o número de páginas na imagem TIFF
            numero_paginas = imagem_tif.n_frames

            for pagina_numero in range(numero_paginas):
                # Carrega a página da imagem
                imagem_tif.seek(pagina_numero)
                imagem = imagem_tif.copy()

                # Converte para preto e branco
                imagem_pb = imagem.convert("L")

                # Define o caminho de destino
                caminho_destino = os.path.join(diretorio_destino, f"pb_{arquivo}_pagina{pagina_numero + 1}.tif")

                # Salva a imagem no diretório de destino
                imagem_pb.save(caminho_destino)

                print(f"Imagem convertida: {caminho_destino}")

if __name__ == "__main__":
    # Substitua 'diretorio_x' e 'diretorio_y' pelos seus diretórios reais
    diretorio_x = "caminho/do/seu/diretorio_x"
    diretorio_y = "caminho/do/seu/diretorio_y"

    converte_para_pb(diretorio_x, diretorio_y)
