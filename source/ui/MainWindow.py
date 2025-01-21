from PySide6.QtWidgets import QMainWindow, QWidget, QStackedWidget, QSplitter,\
    QMenu, QListWidgetItem
from PySide6.QtCore import Qt

from core.QtAddOns import QFriendWidget

from .QNavigationBar import QNavigationBar

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
        self.fichier = QMenu(self.menu_bar)
        self.fichier.setTitle("Fichier")
        self.menu_bar.addMenu(self.fichier)
        self.setMenuBar(self.menu_bar)
        
        self.navbar = QNavigationBar(self)
        self.navbar.setStyleSheet("background-color: blue;")

        item = QListWidgetItemId()
        item.setData(0, "Coucou")
        self.navbar.addItem(item, lambda: print("Bonjour"))

        self.caisse_widget = QFriendWidget()
        self.caisse_widget.setStyleSheet("QWidget:hover { background-color: yellow; } QWidget { background-color: transparent; margin: 0px; padding: 0px; } ")
        self.navbar.addWidget(self.caisse_widget, lambda: print("Au revoir"))
        self.body = QStackedWidget(self)
        self.body.setStyleSheet("background-color: red;")
        
        self.splitter = QSplitter(self)
        self.splitter.insertWidget(0, self.navbar)
        self.splitter.insertWidget(1, self.body)

        
        self.splitter.setSizes([1, 5])

        self.setCentralWidget(self.splitter)

        self.showMaximized()
