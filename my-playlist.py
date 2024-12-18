import os
import vlc
import tkinter as tk
from tkinter import filedialog, messagebox
import youtube_dl
import xml.etree.ElementTree as ET

# Caminho da DLL do VLC no Windows 10 (ajuste o caminho conforme o local onde o VLC está instalado)
vlc_dll_path = r"C:\Program Files\VideoLAN\VLC\libvlc.dll"

# Inicializa o VLC player com o caminho da DLL
if not os.path.exists(vlc_dll_path):
    raise FileNotFoundError(f"A DLL do VLC não foi encontrada no caminho especificado: {vlc_dll_path}")

# Configura o VLC para usar a DLL especificada
Instance = vlc.Instance()
player = Instance.media_player_new()

# Nome do ficheiro XML para a playlist
playlist_xml = "playlist.xml"

# Função para criar uma nova playlist em XML
def criar_playlist():
    playlist = ET.Element("playlist")  # Elemento raiz
    tree = ET.ElementTree(playlist)
    tree.write(playlist_xml)
    messagebox.showinfo("Playlist", "Nova playlist XML criada.")

# Função para adicionar uma stream ao XML
def adicionar_stream(url):
    if not os.path.exists(playlist_xml):
        criar_playlist()

    tree = ET.parse(playlist_xml)
    root = tree.getroot()
    
    stream = ET.Element("stream")
    stream.text = url
    root.append(stream)
    
    tree.write(playlist_xml)
    messagebox.showinfo("Playlist", "Stream adicionada à playlist XML.")

# Função para apagar a playlist XML
def apagar_playlist():
    if os.path.exists(playlist_xml):
        os.remove(playlist_xml)
        messagebox.showinfo("Playlist", "Playlist XML apagada.")
    else:
        messagebox.showinfo("Playlist", "Não existe playlist para apagar.")

# Função para ler a playlist do ficheiro XML
def ler_playlist():
    if not os.path.exists(playlist_xml):
        messagebox.showinfo("Playlist", "A playlist XML está vazia.")
        return []

    tree = ET.parse(playlist_xml)
    root = tree.getroot()

    playlist = []
    for stream in root.findall("stream"):
        playlist.append(stream.text.strip())
    
    return playlist

# Função para tocar a primeira stream na playlist
def tocar_stream():
    playlist = ler_playlist()
    if playlist:
        stream_url = playlist[0]  # Usa o primeiro URL da lista
        try:
            with youtube_dl.YoutubeDL() as ydl:
                info_dict = ydl.extract_info(stream_url, download=False)
                video_url = info_dict['url']
                player.set_mrl(video_url)
                player.play()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível tocar a stream: {str(e)}")
    else:
        messagebox.showinfo("Playlist", "A playlist está vazia.")

# Função para abrir um ficheiro e adicionar o caminho ao XML
def escolher_ficheiro():
    url = filedialog.askopenfilename(title="Escolher ficheiro", filetypes=(("MP4 Files", "*.mp4"), ("Todos os ficheiros", "*.*")))
    adicionar_stream(url)

# Função para sair da aplicação
def sair():
    player.stop()
    root.quit()

# Criação da janela principal com Tkinter
root = tk.Tk()
root.title("Leitor YouTube com VLC e XML")

# Botões
btn_criar_playlist = tk.Button(root, text="Criar Playlist XML", command=criar_playlist)
btn_criar_playlist.pack()

btn_adicionar_stream = tk.Button(root, text="Adicionar Stream XML", command=lambda: adicionar_stream("https://www.youtube.com/watch?v=example"))
btn_adicionar_stream.pack()

btn_escolher_ficheiro = tk.Button(root, text="Escolher Ficheiro", command=escolher_ficheiro)
btn_escolher_ficheiro.pack()

btn_apagar_playlist = tk.Button(root, text="Apagar Playlist XML", command=apagar_playlist)
btn_apagar_playlist.pack()

btn_tocar_stream = tk.Button(root, text="Tocar Stream XML", command=tocar_stream)
btn_tocar_stream.pack()

btn_sair = tk.Button(root, text="Sair", command=sair)
btn_sair.pack()

# Menu
menu = tk.Menu(root)
root.config(menu=menu)
file_menu = tk.Menu(menu)
menu.add_cascade(label="Ficheiro", menu=file_menu)
file_menu.add_command(label="Criar Playlist XML", command=criar_playlist)
file_menu.add_command(label="Adicionar Stream XML", command=lambda: adicionar_stream("https://www.youtube.com/watch?v=example"))
file_menu.add_separator()
file_menu.add_command(label="Sair", command=sair)

# Inicia a interface gráfica
root.mainloop()
