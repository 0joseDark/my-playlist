import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import vlc
import webbrowser
from xml.etree import ElementTree as ET

# Configuração do VLC com caminho da DLL
caminho_dll_vlc = r"C:\Users\jose\Documents\GitHub\my-playlist\vlc\libvlc.dll"
os.environ['PYTHON_VLC_LIB_PATH'] = caminho_dll_vlc

# Inicializa a interface Tkinter
class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Leitor de YouTube com Playlist")
        
        # Configurações da janela
        self.root.geometry("800x600")
        
        # Variável para armazenar URL
        self.url = ""
        
        # Adiciona Menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        
        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Ficheiro", menu=file_menu)
        file_menu.add_command(label="Abrir URL", command=self.abrir_url_e_tocar)
        file_menu.add_command(label="Abrir Ficheiro", command=self.abrir_ficheiro)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)

        # Botão para abrir o navegador
        browser_btn = tk.Button(self.root, text="Abrir YouTube no Navegador", command=self.abrir_navegador)
        browser_btn.pack(pady=10)
        
        # Botão para carregar a playlist
        load_btn = tk.Button(self.root, text="Carregar Playlist", command=self.carregar_playlist)
        load_btn.pack(pady=10)
        
        # Botão para reproduzir mídia
        play_btn = tk.Button(self.root, text="Reproduzir Playlist", command=self.reproduzir_playlist)
        play_btn.pack(pady=10)

    def abrir_url_e_tocar(self):
        # Abrir uma caixa de diálogo para digitar o URL do vídeo
        url = simpledialog.askstring("Abrir URL", "Digite o URL do YouTube:")
        if url:
            self.url = url
            self.adicionar_url_a_playlist(self.url)

    def abrir_ficheiro(self):
        # Função para abrir ficheiro do sistema
        ficheiro = filedialog.askopenfilename(title="Abrir Ficheiro de Vídeo", filetypes=[("Arquivos de vídeo", "*.mp4 *.mkv")])
        if ficheiro:
            self.adicionar_url_a_playlist(ficheiro)

    def adicionar_url_a_playlist(self, url):
        # Adicionar URL à playlist (ficheiro XML)
        playlist_xml = "playlist.xml"
        if not os.path.exists(playlist_xml):
            root = ET.Element("playlist")
        else:
            tree = ET.parse(playlist_xml)
            root = tree.getroot()
        
        stream = ET.Element("stream")
        stream.text = url
        root.append(stream)
        
        tree = ET.ElementTree(root)
        with open(playlist_xml, "wb") as file:
            tree.write(file)
        
        messagebox.showinfo("Sucesso", f"URL {url} adicionada à playlist")

    def carregar_playlist(self):
        # Carregar a playlist do ficheiro XML e exibir
        if os.path.exists("playlist.xml"):
            tree = ET.parse("playlist.xml")
            root = tree.getroot()
            urls = [stream.text for stream in root.findall("stream")]
            messagebox.showinfo("Playlist", "\n".join(urls))
        else:
            messagebox.showerror("Erro", "Nenhuma playlist encontrada")

    def reproduzir_playlist(self):
        # Reproduzir mídia da playlist
        if os.path.exists("playlist.xml"):
            tree = ET.parse("playlist.xml")
            root = tree.getroot()
            urls = [stream.text for stream in root.findall("stream")]
            if urls:
                instancia_vlc = vlc.Instance()
                player = instancia_vlc.media_player_new()
                media = instancia_vlc.media_new(urls[0])  # Toca o primeiro item da playlist
                player.set_media(media)
                player.play()
            else:
                messagebox.showerror("Erro", "Nenhum URL na playlist")
        else:
            messagebox.showerror("Erro", "Nenhuma playlist encontrada")

    def abrir_navegador(self):
        # Abre o navegador padrão para navegar no YouTube
        webbrowser.open("https://www.youtube.com")

# Função principal
if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
