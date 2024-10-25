import sys
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, QAction, QLineEdit, 
                             QVBoxLayout, QListWidget, QDialog, QPushButton, QFileDialog, 
                             QMessageBox)
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

# Função para carregar e exibir a playlist
def carregar_playlist():
    if os.path.exists(playlist_xml):
        tree = ET.parse(playlist_xml)
        root = tree.getroot()
        urls = [stream.text for stream in root.findall("stream")]
        return urls
    return []

# Classe principal do navegador com integração à playlist
class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navegador YouTube com Playlist")
        self.setGeometry(100, 100, 1200, 800)

        # Configuração de abas
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

        # Botão para ir para o YouTube
        youtube_btn = QAction("Abrir YouTube", self)
        youtube_btn.triggered.connect(self.abrir_youtube)
        self.navbar.addAction(youtube_btn)

        # Botão para adicionar URL à playlist
        add_playlist_btn = QAction("Adicionar à Playlist", self)
        add_playlist_btn.triggered.connect(self.adicionar_a_playlist)
        self.navbar.addAction(add_playlist_btn)

        # Botão para carregar a playlist
        load_playlist_btn = QAction("Carregar Playlist", self)
        load_playlist_btn.triggered.connect(self.exibir_playlist)
        self.navbar.addAction(load_playlist_btn)

        # Botão para reproduzir a playlist
        play_playlist_btn = QAction("Reproduzir Playlist", self)
        play_playlist_btn.triggered.connect(self.reproduzir_playlist)
        self.navbar.addAction(play_playlist_btn)

        # Atualiza a URL quando muda de página
        self.browser.urlChanged.connect(self.atualizar_url)

    def abrir_youtube(self):
        # Abre o YouTube na aba atual
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

    def exibir_playlist(self):
        # Carrega e exibe a playlist
        urls = carregar_playlist()
        if urls:
            QMessageBox.information(self, "Playlist", "\n".join(urls))
        else:
            QMessageBox.warning(self, "Playlist", "A playlist está vazia.")

    def reproduzir_playlist(self):
        # Carrega e reproduz a playlist usando o VLC
        urls = carregar_playlist()
        if urls:
            instancia_vlc = vlc.Instance()
            player = instancia_vlc.media_player_new()
            for url in urls:
                media = instancia_vlc.media_new(url)
                player.set_media(media)
                player.play()
                # Aguarda a reprodução de cada vídeo
                while player.get_state() != vlc.State.Ended:
                    QApplication.processEvents()
        else:
            QMessageBox.warning(self, "Reproduzir Playlist", "A playlist está vazia.")

# Função principal
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
