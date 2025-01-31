from __future__ import annotations

from PySide6.QtWidgets import (QListWidget, QWidget, QListView, 
    QListWidgetItem, QLabel, QStyledItemDelegate, QStyleOptionViewItem, QStyle)
from PySide6.QtGui import QMouseEvent, QColor, QPainter
from PySide6.QtCore import (QFileInfo, QDir, QJsonDocument, Signal, 
    QJsonValue, QSize, Qt, QModelIndex, QPersistentModelIndex)

from core.Produit import ProduitData

from os.path import exists as os_exists


class CustomDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex):
        # TODO: on selected
        # Appeler la méthode de base pour conserver le style par défaut
        if QStyle.StateFlag.State_Selected in option.state :
            option.state = option.state & ~QStyle.StateFlag.State_Selected
        super().paint(painter, option, index)

        # painter.save()
        # pen = painter.pen()
        # pen.setColor(Qt.red)
        # painter.setPen(pen)
        # painter.drawRect(option.rect.adjusted(1, 1, -1, -1))
        # print("option", option.state)
        # painter.restore()
    
    def sizeHint(self, option, index):
        # return super().sizeHint(option, index)
        return QSize(200, 250)


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
    produitClicked = Signal(ProduitData)

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
            /* removing the focus selection */
            QListWidget::item:focus {
                color: black;
            }
            QListView
            {
                outline: none;
            }
        """)
        # https://forum.qt.io/topic/18888/how-to-remove-focus-rectangle-on-qlistview-and-similar-using-qstyleditemdelegate-with-style-sheets/12

        self.setFlow(QListView.Flow.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setItemAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.setSelectionRectVisible(False)
        self.setSpacing(5)

        self.setItemDelegate(CustomDelegate(self))
        # 
        self.itemClicked.connect(lambda item: self.produitClicked.emit(item.data(-1)))
        self.itemDoubleClicked.connect(lambda item: self.produitClicked.emit(item.data(-1)))

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
            # item = QListWidgetItem(self)
            # w = Vignette(self)
            # w.setTitre(key)
            # w.setColor(value["color"])
            # item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            # item.setSizeHint(w.sizeHint())
            # self.setItemWidget(item, w)

            item = QListWidgetItem(self)
            item.setData(Qt.ItemDataRole.DisplayRole, key)
            p = ProduitData(nom=key, prix=value["price"], color=value["color"])
            item.setData(-1, p)
            colour = QColor(value["color"])
            # print(colour)
            item.setData(Qt.ItemDataRole.DecorationRole, colour)
            item.setData(Qt.ItemDataRole.TextAlignmentRole, Qt.AlignmentFlag.AlignCenter)
            self.addItem(item)
    
    def minimumSizeHint(self):
        # return super().minimumSizeHint()
        return QSize(0, 0)


class Vignette(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setFixedSize(200, 250)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: red;")

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
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() is Qt.MouseButton.LeftButton:
            # print(self.titre_label.text())
            pass

        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() is Qt.MouseButton.LeftButton:
            pass
        
        return super().mouseReleaseEvent(event)
    
    def sizeHint(self):
        # return super().sizeHint()
        return self.size()
