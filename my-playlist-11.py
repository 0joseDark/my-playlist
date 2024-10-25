import sys
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, QAction, QLineEdit, 
                             QListWidget, QMessageBox, QInputDialog)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from xml.etree import ElementTree as ET

# Caminho para o ficheiro XML da playlist
playlist_xml = "playlist.xml"

# Funções para manipular a playlist XML
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
        self.setWindowTitle("Navegador e Gerenciador de Playlist YouTube")
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

        # Botão para ir para o YouTube
        youtube_btn = QAction("Ir para YouTube", self)
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
        self.lista_streams.itemDoubleClicked.connect(self.carregar_stream_selecionada)

    def criar_menu(self):
        # Menu para abrir URLs e listar playlist
        menu_ficheiro = self.menu.addMenu("Playlist")

        abrir_playlist_action = QAction("Mostrar Playlist", self)
        abrir_playlist_action.triggered.connect(self.mostrar_lista_playlist)
        menu_ficheiro.addAction(abrir_playlist_action)

        adicionar_url_action = QAction("Adicionar URL Manualmente", self)
        adicionar_url_action.triggered.connect(self.adicionar_url_manual)
        menu_ficheiro.addAction(adicionar_url_action)

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

    def adicionar_url_manual(self):
        # Adiciona uma URL à playlist através de um diálogo
        url, ok = QInputDialog.getText(self, "Adicionar URL", "Digite a URL do vídeo:")
        if ok and url:
            adicionar_url_a_playlist(url)
            QMessageBox.information(self, "Playlist", f"URL {url} adicionada à playlist")

    def mostrar_lista_playlist(self):
        # Carrega e exibe a lista de URLs da playlist
        urls = carregar_playlist()
        self.lista_streams.clear()
        self.lista_streams.addItems(urls)
        self.setCentralWidget(self.lista_streams)

    def carregar_stream_selecionada(self):
        # Carrega e exibe o vídeo do YouTube selecionado na lista de streams
        item = self.lista_streams.currentItem()
        if item:
            url = item.text()
            self.browser.setUrl(QUrl(url))
            self.setCentralWidget(self.browser)  # Volta para o navegador para exibir o vídeo

# Função principal
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
