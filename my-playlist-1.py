import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import xml.etree.ElementTree as ET
import ctypes
import vlc
import pywebview  # PyWebview para embutir o browser


# Função para adicionar FFmpeg ao PATH e criar a pasta se necessário
def adicionar_ffmpeg_ao_path():
    caminho_ffmpeg = r"C:\ffmpeg"
    if not os.path.exists(caminho_ffmpeg):
        os.makedirs(caminho_ffmpeg)
        print(f"Pasta criada: {caminho_ffmpeg}")
    else:
        print(f"A pasta já existe: {caminho_ffmpeg}")

    root = tk.Tk()
    root.withdraw()
    resposta = ctypes.windll.user32.MessageBoxW(0, "Deseja copiar os ficheiros FFmpeg para a nova pasta?", "Copiar ficheiros", 0x04 | 0x20)

    if resposta == 6:
        origem_ffmpeg = filedialog.askdirectory(title="Selecione a pasta de origem dos ficheiros 'bin' do FFmpeg")
        if origem_ffmpeg and os.path.exists(origem_ffmpeg):
            destino_bin = os.path.join(caminho_ffmpeg, 'bin')
            if not os.path.exists(destino_bin):
                os.makedirs(destino_bin)
                print(f"Pasta 'bin' criada em: {destino_bin}")

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
            return

    print("Por favor, selecione a pasta 'bin' do FFmpeg.")
    caminho_bin = filedialog.askdirectory(title="Selecione a pasta 'bin' do FFmpeg")
    if not caminho_bin or not os.path.exists(caminho_bin):
        print("Nenhuma pasta selecionada ou caminho inválido.")
        return

    variavel_path = os.environ['PATH']
    if caminho_bin not in variavel_path:
        comando = f'setx PATH "{variavel_path};{caminho_bin}"'
        subprocess.run(comando, shell=True, check=True)
        print(f"FFmpeg foi adicionado ao PATH: {caminho_bin}")
    else:
        print(f"O caminho do FFmpeg já está presente no PATH: {caminho_bin}")

    ctypes.windll.user32.MessageBoxW(0, "O caminho da pasta 'bin' do FFmpeg foi adicionado ao PATH com sucesso!", "Sucesso", 0x40)


# Função para tocar vídeos a partir da playlist
def tocar_video(url):
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(url)
    player.set_media(media)
    player.play()
    print(f"Tocando: {url}")


# Função para abrir o browser e escolher URL
def abrir_browser():
    def navegador_callback(url):
        if url:
            print(f"URL selecionada: {url}")
            adicionar_url_playlist(url)

    window = pywebview.create_window('Navegar pelo YouTube', 'https://www.youtube.com')
    pywebview.start(navegador_callback, window)


# Função para adicionar URL à playlist
def adicionar_url_playlist(url):
    playlist_file = "playlist.xml"
    if not os.path.exists(playlist_file):
        root = ET.Element("playlist")
    else:
        tree = ET.parse(playlist_file)
        root = tree.getroot()

    video = ET.SubElement(root, "video")
    video.set("url", url)

    tree = ET.ElementTree(root)
    with open(playlist_file, "wb") as f:
        tree.write(f)

    print(f"URL {url} adicionada à playlist")


# Função para ler e tocar vídeos da playlist
def tocar_playlist():
    playlist_file = "playlist.xml"
    if not os.path.exists(playlist_file):
        print("A playlist está vazia!")
        return

    tree = ET.parse(playlist_file)
    root = tree.getroot()

    for video in root.findall("video"):
        url = video.get("url")
        tocar_video(url)


# Função para criar a interface gráfica
def criar_interface():
    root = tk.Tk()
    root.title("Leitor de YouTube com Playlist")

    # Botão para abrir o browser e selecionar vídeos
    btn_browser = tk.Button(root, text="Abrir YouTube", command=abrir_browser)
    btn_browser.pack(pady=10)

    # Botão para tocar a playlist
    btn_tocar_playlist = tk.Button(root, text="Tocar Playlist", command=tocar_playlist)
    btn_tocar_playlist.pack(pady=10)

    # Botão para adicionar manualmente uma URL
    btn_adicionar_url = tk.Button(root, text="Adicionar URL Manualmente", command=adicionar_url_manual)
    btn_adicionar_url.pack(pady=10)

    root.mainloop()


# Função para adicionar manualmente URL à playlist
def adicionar_url_manual():
    url = simpledialog.askstring("Adicionar URL", "Digite o URL do vídeo:")
    if url:
        adicionar_url_playlist(url)


if __name__ == "__main__":
    # Adiciona o FFmpeg ao PATH (opcional)
    adicionar_ffmpeg_ao_path()

    # Cria a interface gráfica
    criar_interface()
