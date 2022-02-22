# Mujika - Télécharger des covers en haute qualité !
# Par LDX, Discord="!ldx#0696"
# Version 1.0

from PySide2 import QtWidgets, QtGui, QtCore
import requests

from package.api.api import Deezer, FormatFileName, Download

import sys

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mujika")
        self.setStyleSheet("background-color: #292F3F")
        self.setup_ui()
        
        self.folder_download = str()
        print(self.folder_download)
        self.lt_items_results = list()
        self.item_selected = -1

    def setup_ui(self):
        self.create_layouts()
        self.create_widgets()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()
        self.connect_keyboard_shortcuts()

    def create_widgets(self):
        self.btn_settings = QtWidgets.QPushButton("Options")
        self.lb_app_name = QtWidgets.QLabel()
        self.le_search = QtWidgets.QLineEdit()
        self.btn_search = QtWidgets.QPushButton("Rechercher")
        self.lt_results = QtWidgets.QListWidget()
        self.btn_download = QtWidgets.QPushButton("Télécharger")
        self.preview_image("https://github.com/ldxdev/")


    def modify_widgets(self):
        self.btn_settings.setStyleSheet("""
                color: #F4F9FF;
                background-color: #373E4E;
                border: 0px;     
                border-radius: 5px;   
                padding: 10px;             
        """)
        self.btn_settings.setMaximumWidth(100)
        self.lb_app_name.setText("Mujika - Cover Download")
        self.lb_app_name.setStyleSheet("""
                color : #F4F9FF;  
                padding: 10px;       
        """)
        self.le_search.setPlaceholderText("Nom de l'album ou de l'artiste")
        self.le_search.setStyleSheet("""
                color : #F4F9FF;
                background-color: #373E4E;
                border: 0px;  
                padding: 10px;         
        """)
        self.lt_results.setStyleSheet("""
                color : #F4F9FF;
                background-color: #373E4E;
                border: 0px;       
        """)
        self.btn_search.setStyleSheet("""
                color : #F4F9FF;
                background-color: #4291F9;
                border: 0px;     
                border-radius: 5px;   
                padding: 10px;    
        """)
        self.btn_download.setStyleSheet("""
                color : #F4F9FF;
                background-color: #4291F9;
                border: 0px;  
                border-radius: 5px;   
                padding: 10px;         
        """)

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.settings_title_layout = QtWidgets.QHBoxLayout()
        self.search_layout = QtWidgets.QVBoxLayout()
        self.image_layout = QtWidgets.QVBoxLayout()
        
        self.search_layout.addLayout(self.settings_title_layout)
        self.main_layout.addLayout(self.search_layout)
        self.main_layout.addLayout(self.image_layout)

    def add_widgets_to_layouts(self):
        self.settings_title_layout.addWidget(self.btn_settings)
        self.settings_title_layout.addWidget(self.lb_app_name)
        
        self.search_layout.addWidget(self.le_search)
        self.search_layout.addWidget(self.btn_search)
        self.search_layout.addWidget(self.lt_results)
        self.search_layout.addWidget(self.btn_download)
        
        self.image_layout.addWidget(self.img_preview)


    def setup_connections(self):
        self.btn_settings.clicked.connect(self.window_settings)
        self.btn_search.clicked.connect(self.search_cover)
        self.lt_results.currentRowChanged.connect(self.change_row)
        self.lt_results.itemDoubleClicked.connect(self.download_cover)
        self.btn_download.clicked.connect(self.download_cover)
    
    def connect_keyboard_shortcuts(self):
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self, self.btn_search.clicked.emit)
    
    def window_settings(self):
        self.folder_download = QtWidgets.QFileDialog.getExistingDirectory(self, "Dossier de téléchargement")
    
    def search_cover(self):
        if len(self.le_search.text()) > 0:
            self.lt_results.clear()
            self.lt_items_results.clear()
            self.deezer = Deezer(self.le_search.text()).find_album()
            i = 0
            if not self.deezer == None:
                for album in self.deezer:
                    self.lt_items_results.append(self.deezer[album])
                    self.lt_results.addItem(QtWidgets.QListWidgetItem(f"{self.deezer[album]['title']}, {self.deezer[album]['artist']}"))
                    i = i+1
                
    def change_row(self, currentRow):
        self.item_selected = currentRow
        self.img_preview.deleteLater()
        self.preview_image(self.lt_items_results[self.item_selected]["cover"])
        self.image_layout.addWidget(self.img_preview)
                
    def preview_image(self, url:str):
        image = QtGui.QImage()
        image.loadFromData(requests.get(url=url).content)
        self.img_preview = QtWidgets.QLabel()
        self.img_preview.setPixmap(QtGui.QPixmap(image).scaled(350, 350, QtCore.Qt.KeepAspectRatio))
    
    def download_cover(self):
        if len(self.folder_download) == 0:
            self.window_settings()
        if not self.item_selected == -1:
            Download(url=self.lt_items_results[self.item_selected]["cover"], name=FormatFileName(self.lt_items_results[self.item_selected]["title"], self.lt_items_results[self.item_selected]["artist"]).format_file_name(), folder=self.folder_download).download()