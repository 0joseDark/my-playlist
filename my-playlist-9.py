import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, QAction, QListWidget, 
                             QFileDialog, QMessageBox, QInputDialog)
from PyQt5.QtGui import QIcon
from xml.etree import ElementTree as ET
import vlc

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

def modificar_url_playlist(index, nova_url):
    if os.path.exists(playlist_xml):
        tree = ET.parse(playlist_xml)
        root = tree.getroot()
        streams = root.findall("stream")
        if 0 <= index < len(streams):
            streams[index].text = nova_url
            tree.write(playlist_xml)
            print(f"URL modificada para: {nova_url}")

def apagar_url_playlist(index):
    if os.path.exists(playlist_xml):
        tree = ET.parse(playlist_xml)
        root = tree.getroot()
        streams = root.findall("stream")
        if 0 <= index < len(streams):
            root.remove(streams[index])
            tree.write(playlist_xml)
            print("URL removida da playlist")

# Classe principal da interface gráfica
class PlaylistManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciador de Playlist XML")
        self.setGeometry(100, 100, 600, 400)

        # Lista de streams
        self.lista_streams = QListWidget()
        self.lista_streams.itemDoubleClicked.connect(self.reproduzir_stream_selecionada)
        self.setCentralWidget(self.lista_streams)

        # Barra de ferramentas
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Botão para listar a playlist
        listar_action = QAction("Listar Playlist", self)
        listar_action.triggered.connect(self.mostrar_lista_playlist)
        self.toolbar.addAction(listar_action)

        # Botão para abrir um ficheiro de mídia
        abrir_action = QAction("Abrir Ficheiro", self)
        abrir_action.triggered.connect(self.abrir_ficheiro)
        self.toolbar.addAction(abrir_action)

        # Botão para adicionar uma URL manualmente
        adicionar_url_action = QAction("Adicionar URL", self)
        adicionar_url_action.triggered.connect(self.adicionar_url)
        self.toolbar.addAction(adicionar_url_action)

        # Botão para modificar uma URL
        modificar_url_action = QAction("Modificar URL", self)
        modificar_url_action.triggered.connect(self.modificar_url)
        self.toolbar.addAction(modificar_url_action)

        # Botão para apagar uma URL
        apagar_url_action = QAction("Apagar URL", self)
        apagar_url_action.triggered.connect(self.apagar_url)
        self.toolbar.addAction(apagar_url_action)

    def mostrar_lista_playlist(self):
        # Carrega e exibe a lista de URLs da playlist
        urls = carregar_playlist()
        self.lista_streams.clear()
        self.lista_streams.addItems(urls)

    def abrir_ficheiro(self):
        # Permite ao usuário escolher um ficheiro de vídeo ou som e adiciona à playlist
        ficheiro, _ = QFileDialog.getOpenFileName(self, "Abrir Ficheiro de Mídia", "", "Media Files (*.mp4 *.mp3 *.wav *.mkv)")
        if ficheiro:
            adicionar_url_a_playlist(ficheiro)
            QMessageBox.information(self, "Playlist", f"Ficheiro {ficheiro} adicionado à playlist")
            self.mostrar_lista_playlist()

    def adicionar_url(self):
        # Adiciona uma URL à playlist através de um diálogo
        url, ok = QInputDialog.getText(self, "Adicionar URL", "Digite a URL:")
        if ok and url:
            adicionar_url_a_playlist(url)
            QMessageBox.information(self, "Playlist", f"URL {url} adicionada à playlist")
            self.mostrar_lista_playlist()

    def modificar_url(self):
        # Modifica uma URL selecionada na lista
        selected_row = self.lista_streams.currentRow()
        if selected_row >= 0:
            nova_url, ok = QInputDialog.getText(self, "Modificar URL", "Digite a nova URL:")
            if ok and nova_url:
                modificar_url_playlist(selected_row, nova_url)
                QMessageBox.information(self, "Playlist", "URL modificada com sucesso")
                self.mostrar_lista_playlist()

    def apagar_url(self):
        # Apaga uma URL selecionada da lista
        selected_row = self.lista_streams.currentRow()
        if selected_row >= 0:
            resposta = QMessageBox.question(self, "Apagar URL", "Deseja realmente apagar esta URL?", QMessageBox.Yes | QMessageBox.No)
            if resposta == QMessageBox.Yes:
                apagar_url_playlist(selected_row)
                QMessageBox.information(self, "Playlist", "URL apagada com sucesso")
                self.mostrar_lista_playlist()

    def reproduzir_stream_selecionada(self):
        # Reproduz a URL selecionada usando VLC
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
    window = PlaylistManager()
    window.show()
    sys.exit(app.exec_())
