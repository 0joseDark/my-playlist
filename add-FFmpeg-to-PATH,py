import os
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog
import ctypes

def adicionar_ffmpeg_ao_path():
    # Verifica se a pasta para o FFmpeg já existe, caso contrário, cria a pasta
    caminho_ffmpeg = r"C:\ffmpeg"
    if not os.path.exists(caminho_ffmpeg):
        os.makedirs(caminho_ffmpeg)
        print(f"Pasta criada: {caminho_ffmpeg}")
    else:
        print(f"A pasta já existe: {caminho_ffmpeg}")
    
    # Pergunta ao utilizador se deseja copiar os ficheiros de outra localização
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter
    resposta = ctypes.windll.user32.MessageBoxW(0, "Deseja copiar os ficheiros FFmpeg para a nova pasta?", "Copiar ficheiros", 0x04 | 0x20)

    if resposta == 6:  # O utilizador selecionou "Sim"
        # Abre o explorador de ficheiros para o utilizador selecionar a pasta de origem dos ficheiros FFmpeg
        origem_ffmpeg = filedialog.askdirectory(title="Selecione a pasta de origem dos ficheiros 'bin' do FFmpeg")

        if origem_ffmpeg and os.path.exists(origem_ffmpeg):
            # Copiar ficheiros da pasta 'bin' para o novo diretório
            destino_bin = os.path.join(caminho_ffmpeg, 'bin')
            if not os.path.exists(destino_bin):
                os.makedirs(destino_bin)
                print(f"Pasta 'bin' criada em: {destino_bin}")

            # Copia todos os ficheiros e subdiretórios da pasta origem para a pasta destino
            for item in os.listdir(origem_ffmpeg):
                origem_item = os.path.join(origem_ffmpeg, item)
                destino_item = os.path.join(destino_bin, item)
                if os.path.isdir(origem_item):
                    shutil.copytree(origem_item, destino_item)
                else:
                    shutil.copy2(origem_item, destino_item)
            print(f"Ficheiros copiados de {origem_ffmpeg} para {destino_bin}")
        else:
            print("Nenhuma pasta válida foi selecionada ou caminho inválido.")
            sys.exit(1)
    else:
        print("Copiar ficheiros foi ignorado.")

    # Abre o explorador de ficheiros para o utilizador selecionar a pasta 'bin'
    print("Por favor, selecione a pasta 'bin' do FFmpeg.")
    
    # Janela para o utilizador selecionar a pasta 'bin'
    caminho_bin = filedialog.askdirectory(title="Selecione a pasta 'bin' do FFmpeg")

    # Verificar se o utilizador selecionou a pasta correta
    if not caminho_bin or not os.path.exists(caminho_bin):
        print("Nenhuma pasta selecionada ou caminho inválido.")
        sys.exit(1)
    
    print(f"Pasta 'bin' selecionada: {caminho_bin}")

    # Verifica se o caminho da pasta 'bin' já está nas variáveis de ambiente
    variavel_path = os.environ['PATH']
    if caminho_bin not in variavel_path:
        try:
            # Comando para adicionar às variáveis de ambiente (de forma permanente)
            comando = f'setx PATH "{variavel_path};{caminho_bin}"'
            print(f"A executar: {comando}")

            # Executa o comando no terminal do Windows
            subprocess.run(comando, shell=True, check=True)
            print(f"FFmpeg foi adicionado ao PATH: {caminho_bin}")

        except subprocess.CalledProcessError as e:
            print(f"Erro ao adicionar FFmpeg ao PATH: {e}")
            sys.exit(1)
    else:
        print(f"O caminho do FFmpeg já está presente no PATH: {caminho_bin}")

    # Aviso de que o caminho foi adicionado com sucesso
    ctypes.windll.user32.MessageBoxW(0, "O caminho da pasta 'bin' do FFmpeg foi adicionado ao PATH com sucesso!", "Sucesso", 0x40)

if __name__ == "__main__":
    adicionar_ffmpeg_ao_path()
