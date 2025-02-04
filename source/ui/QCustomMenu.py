from __future__ import annotations

from PySide6.QtWidgets import (QMenuBar, QWidget, QHBoxLayout, QPushButton, 
    QMenu)
from PySide6.QtGui import QResizeEvent, QPixmap, QAction
from PySide6.QtCore import QSize, Qt


class QCustomMenu(QMenuBar):
    def __init__(self: QCustomMenu, parent: QWidget):
        super().__init__(parent)
        self.setStyleSheet(
            """
            QMenuBar {
                min-height: 50px;
                icon-size: 35px;
            }
            QMenuBar::item {
            }
            QMenuBar::item:selected { 
                background-color: #D5D5D5; 
            }
            
            QMenu::item {
                padding: 5px;
                border: none; 
                icon-size: 35px;
            }
            QMenu::item:selected {
                color: black; 
                /*background-color: #D5D5D5; */
            } 
            """
        )
        
        self.menu_burger = QAction(self)
        self.menu_burger.setIcon(QPixmap("assets/burger.svg"))
        # self.menu_burger.setIconSize(QSize(35, 35))
        # self.menu_burger.setGeometry(3, 3, 35, 35)
        # self.menu_burger.setStyleSheet(
        #     """
        #     QPushButton { 
        #         border: none; 
        #         border-radius: 5px; 
        #         background-color: transparent; 
        #     } 
        #     QPushButton::pressed { 
        #         /*padding-top: 3px; 
        #         padding-left: 3px;*/ 
        #         background-color: #CDD0DA; 
        #     }
        #     """)
        self.addAction(self.menu_burger)

        self.fichier = QMenu(self)
        self.fichier.setTitle("Fichier")
        self.quitter = QAction(self.fichier)
        self.quitter.setText("Quitter")
        self.quitter.setShortcut("Ctrl+Q")
        self.quitter.triggered.connect(self.close)
        self.fichier.addAction(self.quitter)
        self.fichier.move(100, 0)

        self.addMenu(self.fichier)
    
    def resizeEvent(self, event: QResizeEvent):
        self.resize(event.size().width(), self.height())
        return super().resizeEvent(event)

    def sizeHint(self):
        # return super().sizeHint()
        return QSize(self.parent().width(), 50)