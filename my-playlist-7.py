import sys
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, QAction, QLineEdit, 
                             QListWidget, QFileDialog, QMessageBox, QMenu, QInputDialog)
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from xml.etree import ElementTree as ET
import vlc

# Caminho para o ficheiro XML da playlist
playlist_xml = "playlist.xml"

# Função para adicionar uma URL à playlist XML
def adicionar_url_a_playlist(url):
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
    print(f"URL adicionada à playlist: {url}")

# Função para carregar a playlist do XML
def carregar_playlist():
    urls = []
    if os.path.exists(playlist_xml):
        tree = ET.parse(playlist_xml)
        root = tree.getroot()
        urls = [stream.text for stream in root.findall("stream")]
    return urls

# Classe principal do navegador e gerenciador de playlist
class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navegador YouTube com Playlist")
        self.setGeometry(100, 100, 1200, 800)

        # Configuração do navegador
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.youtube.com"))
        self.setCentralWidget(self.browser)

        # Configuração da barra de navegação
        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        # Campo de URL
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navegar_para_url)
        self.navbar.addWidget(self.url_bar)

        # Botão para abrir o YouTube
        youtube_btn = QAction("Abrir YouTube", self)
        youtube_btn.triggered.connect(self.abrir_youtube)
        self.navbar.addAction(youtube_btn)

        # Botão para adicionar URL à playlist
        add_playlist_btn = QAction("Adicionar à Playlist", self)
        add_playlist_btn.triggered.connect(self.adicionar_a_playlist)
        self.navbar.addAction(add_playlist_btn)

        # Configuração do Menu
        self.menu = self.menuBar()
        self.criar_menu()

        # Lista de streams da playlist
        self.lista_streams = QListWidget()
        self.lista_streams.itemDoubleClicked.connect(self.reproduzir_stream_selecionada)

    def criar_menu(self):
        # Menu para abrir ficheiros e URL
        menu_ficheiro = self.menu.addMenu("Ficheiro")
        
        abrir_ficheiro_action = QAction("Abrir Ficheiro de Mídia", self)
        abrir_ficheiro_action.triggered.connect(self.abrir_ficheiro)
        menu_ficheiro.addAction(abrir_ficheiro_action)

        abrir_url_action = QAction("Abrir URL", self)
        abrir_url_action.triggered.connect(self.abrir_url)
        menu_ficheiro.addAction(abrir_url_action)

        abrir_xml_action = QAction("Abrir Playlist XML", self)
        abrir_xml_action.triggered.connect(self.mostrar_lista_playlist)
        menu_ficheiro.addAction(abrir_xml_action)

    def abrir_youtube(self):
        # Redefine o navegador para abrir o YouTube
        self.browser.setUrl(QUrl("https://www.youtube.com"))

    def navegar_para_url(self):
        # Navega para a URL digitada
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def atualizar_url(self, qurl):
        # Atualiza a barra de URL com a URL atual
        self.url_bar.setText(qurl.toString())

    def adicionar_a_playlist(self):
        # Adiciona a URL atual do navegador à playlist
        url = self.browser.url().toString()
        adicionar_url_a_playlist(url)
        QMessageBox.information(self, "Playlist", f"URL adicionada à playlist:\n{url}")

    def abrir_ficheiro(self):
        # Permite ao usuário escolher um ficheiro de vídeo ou som
        ficheiro, _ = QFileDialog.getOpenFileName(self, "Abrir Ficheiro de Mídia", "", "Media Files (*.mp4 *.mp3 *.wav *.mkv)")
        if ficheiro:
            adicionar_url_a_playlist(ficheiro)
            QMessageBox.information(self, "Playlist", f"Ficheiro {ficheiro} adicionado à playlist")

    def abrir_url(self):
        # Abre um diálogo para o usuário inserir uma URL e adiciona à playlist
        url, ok = QInputDialog.getText(self, "Abrir URL", "Digite a URL do vídeo ou som:")
        if ok and url:
            adicionar_url_a_playlist(url)
            QMessageBox.information(self, "Playlist", f"URL {url} adicionada à playlist")

    def mostrar_lista_playlist(self):
        # Carrega e exibe a lista da playlist na janela principal
        urls = carregar_playlist()
        if urls:
            self.lista_streams.clear()
            self.lista_streams.addItems(urls)
            self.setCentralWidget(self.lista_streams)
        else:
            QMessageBox.warning(self, "Playlist", "A playlist está vazia.")

    def reproduzir_stream_selecionada(self):
        # Reproduz o item selecionado na lista de streams
        item = self.lista_streams.currentItem()
        if item:
            url = item.text()
            self.reproduzir_midia(url)

    def reproduzir_midia(self, url):
        # Usa o VLC para reproduzir a mídia
        instancia_vlc = vlc.Instance()
        player = instancia_vlc.media_player_new()
        media = instancia_vlc.media_new(url)
        player.set_media(media)
        player.play()
        QMessageBox.information(self, "Reprodução", f"Reproduzindo: {url}")

# Função principal
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
