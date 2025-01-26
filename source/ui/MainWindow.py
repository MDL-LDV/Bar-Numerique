from PySide6.QtWidgets import (QMainWindow, QWidget, QSplitter, QMenu, 
    QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QPixmap

from .QNavigationBar import QNavigationBar
from .QBody import QBody
from .Caisse import CaissePage

from core.QtAddOns import QListWidgetItemId

from typing import Optional

from sys import version
from ctypes import windll


class MainWindow(QMainWindow):
    """
    Parent:
        QMainWindow
    Role:
        pass
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Inputs:
            parent: Optional[QWidget]
                default: None
        Outputs:
            None (ctor)
        """
        super().__init__(parent)

        # Give the app a name
        self.setWindowTitle("Bar numérique")
        self.resize(700, 400)

        # Définit l'icone dans la bar des tâches (en utilisant celle de 
        # l'application) https://stackoverflow.com/a/1552105/15793884
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            f"{self.windowTitle()}_{version}"
        )

        self.menu_bar = self.menuBar()
        burger = QPixmap("assets/burger.svg")
        self.menu_burger = QAction()
        self.menu_burger.setIcon(burger)
        self.menu_bar.addAction(self.menu_burger)
        self.fichier = QMenu(self.menu_bar)
        self.fichier.setTitle("Fichier")
        self.menu_bar.addMenu(self.fichier)
        self.setMenuBar(self.menu_bar)
        
        self.navbar = QNavigationBar(self)
        self.navbar.hide()
        self.menu_burger.triggered.connect(self.navbar.activer)

        item = QListWidgetItemId()
        item.identifiant = "Caisse"
        item.setData(0, "Caisse")
        self.navbar.addItem(item, lambda: print("Caisse"))

        # self.caisse_widget = QWidget()
        # layout = QHBoxLayout(self.caisse_widget)
        # label = QLabel()
        # label.setText("Bonjour")
        # layout.addWidget(label)
        # self.caisse_widget.setStyleSheet(
        #     "QWidget { background-color: transparent; } "
        #     + "QWidget:hover { background-color: yellow; }")
        # self.caisse_widget.setStyleSheet(
        #     "QWidget:hover { background-color: yellow; } "
        #     + "QWidget { background-color: transparent; } ")
        # self.navbar.addWidget(self.caisse_widget, lambda: print("Au revoir"))
        
        self.body = QBody(self)
        self.navbar.pageclicked.connect(self.body.dispatcher)

        self.caisse = CaissePage(self.body)
        self.body.addWidget(self.caisse)

        w = QWidget(self)
        w.setObjectName("coucou")
        w.setStyleSheet("QWidget { background-color: white; border: 2px solid black; }")
        self.body.addWidget(w)
        
        self.splitter = QSplitter(self)
        self.splitter.insertWidget(0, self.navbar)
        self.splitter.insertWidget(1, self.body)
        
        self.splitter.setSizes([1, 1])

        self.setCentralWidget(self.splitter)

        self.showMaximized()
    