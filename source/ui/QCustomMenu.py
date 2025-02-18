from __future__ import annotations

from PySide6.QtWidgets import (QMenuBar, QWidget, QMenu)
from PySide6.QtGui import QResizeEvent, QPixmap, QAction
from PySide6.QtCore import QSize, Qt, Signal

from .QExport import QExport


class QCustomMenu(QMenuBar):
    menuClicked = Signal()
    def __init__(self: QCustomMenu, parent: QWidget):
        super().__init__(parent)
        self.setStyleSheet(
            """
            QMenuBar {
                min-height: 50px;
                font-size: 15px;
            }
            QMenuBar::item {
            }
            QMenuBar::item:selected { 
                background-color: #D5D5D5; 
            }
            QMenu::item {
                padding-top: 5px;
                padding-bottom: 5px;
                padding-right: 10px;
                padding-left: 5px;
                border: none; 
                icon-size: 35px;
                font-size: 15px;
            }
            QMenu::item:selected {
                color: black; 
                background-color: #D5D5D5;
            } 
            """
        )
        
        self.menu_burger = QAction(self)
        self.menu_burger.setIcon(QPixmap("assets/burger.svg"))
        self.menu_burger.triggered.connect(lambda: self.menuClicked.emit())
        self.addAction(self.menu_burger)

        # Fichier
        
        self.fichier = QMenu(self)
        self.fichier.setTitle("Fichier")

        self.exporter_act = QAction(self.fichier)
        self.exporter_act.setText("Exporter...")
        self.exporter_act.setShortcut("Ctrl+E")
        self.exporter_act.triggered.connect(self.exporter)
        self.fichier.addAction(self.exporter_act)
        
        self.quitter_act = QAction(self.fichier)
        self.quitter_act.setText("Quitter")
        self.quitter_act.setShortcut("Ctrl+Q")
        self.quitter_act.triggered.connect(self.parent().close)
        self.fichier.addAction(self.quitter_act)

        self.addMenu(self.fichier)
        self.adjustSize()
    
    def exporter(self: QCustomMenu):
        menu = QExport(self)
        menu.exec()
    
    def resizeEvent(self, event: QResizeEvent):
        self.resize(event.size().width(), self.height())
        return super().resizeEvent(event)

    def sizeHint(self):
        return super().sizeHint()