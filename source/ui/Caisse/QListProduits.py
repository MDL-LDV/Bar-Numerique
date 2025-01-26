from __future__ import annotations

from PySide6.QtWidgets import (QListWidget, QWidget, QListView, 
    QListWidgetItem, QLabel)
from PySide6.QtCore import (QFileInfo, QFile, QDir, QJsonDocument, QJsonArray, 
    QJsonValue, QSize, Qt)
from PySide6.QtGui import QColor

from os.path import exists as os_exists

from typing import Optional


def get_chemin(filename: str, dirname: str = "") -> str | None:
    #! TODO: optimiser la fonction, retirer les erreurs en créant le fichier
    path: QDir = QFileInfo(__file__).absoluteDir()

    if not dirname:
        while not os_exists(path.path() + filename) and path != path.root():
            path.cdUp()
    
        if path != path.root():
            return path.filePath(filename)
        else:
            raise NameError(f"{filename} does not exists")
    else:
        # while path.dirName() != dirname and path != path.root():
        #     path.cdUp()

        #     print(path.path() == path.root().path())

        index = path.path().find("/" + dirname + "/") + 1
        if index > 0:
            path = path.path()[:index] + dirname + "/" + filename
            
            if os_exists(path):
                return path
            else:
                raise NameError(f"File {filename} does not exist in the {dirname} directory")
        else:
            raise NameError(f"Directory {dirname} does not exist")


class QListProduits(QListWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.chemin_fichier_produits = get_chemin("produits.json", "source")
        self.fichier_produits: QJsonDocument
        self.produits: dict = {}

        self.get_produits()
        self.setStyleSheet(
            """QListWidget {
                font: bold 20px; 
            }
            QListWidget::item { 
                background-color: transparent; 
                border: 2px solid black; 
                border-radius: 20px; 
            }
            QListWidget::item {
                border-radius: 20px; 
                background: transparent;
            }
            QListView::item:focus{
                background-color: yellow;
            }
        """)
        # https://forum.qt.io/topic/18888/how-to-remove-focus-rectangle-on-qlistview-and-similar-using-qstyleditemdelegate-with-style-sheets/12

        self.setFlow(QListView.Flow.LeftToRight)
        self.setWrapping(True)
        # self.setViewMode(QListView.ViewMode.IconMode)
        self.setSelectionRectVisible(False)
        self.setSpacing(5)
        self.itemClicked.connect(self.add_produit)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setItemAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.fill()

    def get_produits(self: QListProduits) -> None:
        with open(self.chemin_fichier_produits, mode="rb") as file:
            data = file.read()
            file.close()
        
        self.fichier_produits = QJsonDocument.fromJson(data)
        self.produits = self.fichier_produits.object()
    
    def fill(self: QListProduits) -> None:
        #! TODO: dataclass pour les produits et donc retirer qt de la gestion des fichiers

        self.clear()
        for key, value in self.produits.items():
            # print(f"{key}: {value}")
            item = QListWidgetItem(self)

            w = Vignette(self)
            w.setTitre(key)
            w.setColor(value["color"])
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            
            item.setSizeHint(w.sizeHint())
            self.setItemWidget(item, w)
    
    def minimumSizeHint(self):
        # return super().minimumSizeHint()
        return QSize(0, 0)
    
    def focusInEvent(self, event):
        if event.reason() is not Qt.FocusReason.MouseFocusReason:
            self.clearFocus()

        return super().focusInEvent(event)
    
    def mouseDoubleClickEvent(self, event):
        self.clearFocus()
        return super().mouseDoubleClickEvent(event)
    
    def mousePressEvent(self, event):
        if event.button() is Qt.MouseButton.RightButton:
            self.clearFocus()
        return super().mousePressEvent(event)

    def add_produit(self, item: QListWidgetItem) -> None:
        item.setSelected(False)
        self.clearFocus()
        
        # index = self.indexFromItem(item)
        print(self.itemWidget(item).titre_label.text())


class Vignette(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setFixedSize(200, 250)
        self.setStyleSheet("QWidget { background-color: transparent; } QWidget:selected {  }")

        self.image_label = QLabel(self)
        self.image_label.setGeometry(10, 10, 176, 160)
        self.image_label_style = "border-radius: 10px;"
        self.image_label.setStyleSheet(self.image_label_style)
        
        self.titre_label = QLabel(self)
        self.titre_label.setStyleSheet("font-size: 16px;")
        self.titre_label.setGeometry(8, 175, 180, 20)
    
    def setTitre(self, titre: str) -> None:
        self.titre_label.setText(titre)
    
    def setColor(self, color: str) -> None:
        self.image_label.setStyleSheet(
            f"{self.image_label_style} background-color: {color};")
    
    def sizeHint(self):
        # return super().sizeHint()
        return self.size()
