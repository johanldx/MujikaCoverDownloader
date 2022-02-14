# Mujika - Télécharger des covers en haute qualité !
# Par LDX, Discord="!ldx#0696"
# Version 1.0

from PySide2 import QtWidgets, QtGui, QtCore

from package.api.api import Deezer, FormatFileName, Download

import sys

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mujika")
        self.setStyleSheet("background-color: #292F3F")
        self.setup_ui()
        
        self.lt_items_results = list()
        self.item_selected = -1

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()
        self.connect_keyboard_shortcuts()

    def create_widgets(self):
        self.lb_app_name = QtWidgets.QLabel()
        self.le_search = QtWidgets.QLineEdit()
        self.btn_search = QtWidgets.QPushButton("Rechercher")
        self.lt_results = QtWidgets.QListWidget()
        self.btn_download = QtWidgets.QPushButton("Télécharger")

    def modify_widgets(self):
        self.lb_app_name.setText("Mujika - Cover Download")
        self.lb_app_name.setStyleSheet("""
                color : #ffffff;  
                padding: 10px;       
        """)
        self.le_search.setPlaceholderText("Nom de l'album")
        self.le_search.setStyleSheet("""
                color : #ffffff;
                background-color: #373E4E;
                border: 0px;  
                padding: 10px;         
        """)
        self.lt_results.setStyleSheet("""
                color : #ffffff;
                background-color: #373E4E;
                border: 0px;       
        """)
        self.btn_search.setStyleSheet("""
                color : #ffffff;
                background-color: #03A9F1;
                border: 0px;     
                border-radius: 5px;   
                padding: 10px;    
        """)
        self.btn_download.setStyleSheet("""
                color : #ffffff;
                background-color: #03A9F1;
                border: 0px;  
                border-radius: 5px;   
                padding: 10px;         
        """)

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.lb_app_name)
        self.main_layout.addWidget(self.le_search)
        self.main_layout.addWidget(self.btn_search)
        self.main_layout.addWidget(self.lt_results)
        self.main_layout.addWidget(self.btn_download)


    def setup_connections(self):
        self.btn_search.clicked.connect(self.search_cover)
        self.lt_results.currentRowChanged.connect(self.change_row)
        self.lt_results.itemDoubleClicked.connect(self.download_cover)
        self.btn_download.clicked.connect(self.download_cover)
    
    def connect_keyboard_shortcuts(self):
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self, self.btn_search.clicked.emit)
    
    def search_cover(self):
        if len(self.le_search.text()) > 0:
            self.lt_results.clear()
            self.deezer = Deezer(self.le_search.text()).find_album()
            i = 0
            if not self.deezer == None:
                for album in self.deezer:
                    self.lt_items_results.append(self.deezer[album])
                    self.lt_results.addItem(QtWidgets.QListWidgetItem(f"{self.deezer[album]['title']}, {self.deezer[album]['artist']}"))
                    i = i+1
                
    def change_row(self, currentRow):
        self.item_selected = currentRow
                
    def download_cover(self):
        if not self.item_selected == -1:
            Download(self.lt_items_results[self.item_selected]["cover"], FormatFileName(self.lt_items_results[self.item_selected]["title"], self.lt_items_results[self.item_selected]["artist"]).format_file_name()).download()