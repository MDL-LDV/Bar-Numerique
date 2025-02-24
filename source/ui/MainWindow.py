from PySide6.QtWidgets import QMainWindow, QWidget

from .QNavigationBar import QNavigationBar
from .QCustomMenu import QCustomMenu
from .QBody import QBody
from .Caisse import CaissePage
from .Historique import HistoriquePage

from core.QtAddOns import QListWidgetItemId, QRatioSlitter

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
        self.setStyleSheet("background-color: white;")

        # Définit l'icone dans la bar des tâches (en utilisant celle de 
        # l'application) https://stackoverflow.com/a/1552105/15793884
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            f"{self.windowTitle()}_{version}"
        )
        
        self.menu = QCustomMenu(self)
        self.setMenuBar(self.menu)
        
        self.navbar = QNavigationBar(self)
        self.navbar.hide()
        self.menu.menuClicked.connect(self.navbar.actionner)

        item = QListWidgetItemId()
        item.identifiant = "Caisse"
        item.setData(0, "Caisse")
        self.navbar.addItem(item)

        item = QListWidgetItemId()
        item.identifiant = "Historique"
        item.setData(0, "Historique")
        self.navbar.addItem(item)

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

        self.historique = HistoriquePage(self.body)
        self.body.addWidget(self.historique)
        self.body.setCurrentIndex(1)
        
        self.splitter = QRatioSlitter(self)
        self.splitter.insertWidget(0, self.navbar)
        self.splitter.insertWidget(1, self.body)
        
        self.splitter.setSizes([1, 6])

        self.setCentralWidget(self.splitter)
        self.setMinimumWidth(self.body.minimumWidth())
        self.setMinimumHeight(
            self.menuBar().height()
            + self.body.minimumHeight()
        )

        self.showMaximized()
    