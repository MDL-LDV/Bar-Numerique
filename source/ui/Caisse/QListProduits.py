from __future__ import annotations

from PySide6.QtWidgets import (QListWidget, QWidget, QListView, 
    QListWidgetItem, QLabel, QStyledItemDelegate, QStyleOptionViewItem, QStyle, 
    QApplication, QDialog)
from PySide6.QtGui import QMouseEvent, QColor, QPainter, QFont
from PySide6.QtCore import (QFileInfo, QDir, QJsonDocument, Signal, 
    QAbstractItemModel, QSize, Qt, QModelIndex, QPersistentModelIndex, QRect)
from decimal import Decimal

from core.Produit import ProduitData
from core.core import get_produit

from os.path import exists as os_exists
import sys

p = []

def print_unique(key, *args, **kwargs):
    global p
    if key not in p:
        print(*args, **kwargs)
        p.append(key)


class CustomDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex):
        self.initStyleOption(option, index)
        painter.save()

        widget: QWidget = option.widget
        style: QStyle = widget.style() if widget else QApplication.style()
        proxy = style.proxy
        listWidget: QListProduits = self.parent()
        item = listWidget.itemFromIndex(index)

        # TODO: on selected
        if QStyle.StateFlag.State_Selected in option.state :
            option.state = (option.state & ~QStyle.StateFlag.State_Selected 
                            & ~QStyle.StateFlag.State_HasFocus)
        
        # print_unique(1, option.__dir__())

        option.decorationPosition = QStyleOptionViewItem.Position.Top
        decorationRect: QRect = option.rect.adjusted(15, 15, -15, -100)
        option.decorationSize = decorationRect.size()
        painter.setBrush(item.data(Qt.ItemDataRole.DecorationRole))
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.GlobalColor.transparent)
        painter.drawRoundedRect(decorationRect, 10, 10, Qt.SizeMode.AbsoluteSize)

        nomRect = option.rect.adjusted(15, 30 + decorationRect.height(), -15, -15)
        prixRect = option.rect.adjusted(15, 60 + decorationRect.height(), -15, -15)
        
        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(nomRect, item.data(Qt.ItemDataRole.DisplayRole), Qt.AlignmentFlag.AlignLeft)
        painter.setPen(QColor(0, 47, 203, 255))
        f = QFont()
        f.setPixelSize(17)
        painter.setFont(f)
        painter.drawText(prixRect, str(item.data(-1).prix) + " €", Qt.AlignmentFlag.AlignLeft)

        painter.setBrush(Qt.GlobalColor.transparent)
        painter.setPen(Qt.GlobalColor.black)
        painter.drawRoundedRect(option.rect.adjusted(1, 1, -1, -1), 25, 25, Qt.SizeMode.AbsoluteSize)
        """
        iconRect = proxy().subElementRect(QStyle.SubElement.SE_ItemViewItemDecoration, option, widget)
        option.icon.paint(painter, iconRect, option.decorationAlignment, QIcon.Mode.Normal, QIcon.State.On)
        """

        painter.restore()
        # super().paint(painter, option, index)
        """
['__new__', '__init__', '__copy__', 'displayAlignment', 'decorationAlignment', 
'textElideMode', 'decorationPosition', 'decorationSize', 'font', 'showDecorationSelected', 
'features', 'locale', 'widget', 'index', 'checkState', 'icon', 'text', 'viewItemPosition', 
'backgroundBrush', '__doc__', '__module__', 'StyleOptionType', 'StyleOptionVersion', 
'Position', 'ViewItemFeature', 'ViewItemPosition', '__repr__', 'initFrom', 
'version', 'type', 'state', 'direction', 'rect', 'fontMetrics', 'palette', 
'styleObject', 'OptionType', '__getattribute__', '__setattr__', '__delattr__', 
'__dict__', '__hash__', '__str__', '__lt__', '__le__', '__eq__', '__ne__', 
'__gt__', '__ge__', '__reduce_ex__', '__reduce__', '__getstate__', 
'__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', 
'__class__']
        """
    
    def sizeHint(self, option, index):
        # return super().sizeHint(option, index)
        return QSize(200, 250)
    
    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex | QPersistentModelIndex):
        print(editor, model)
        return super().setModelData(editor, model, index)


class QListProduits(QListWidget):
    produitClicked = Signal(ProduitData)

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.chemin_fichier_produits = sys.path[0] + "\\produits.json"
        self.fichier_produits: QJsonDocument
        self.list_produit: list[ProduitData] = get_produit()
        self.setStyleSheet(
            """QListWidget {
                font: bold 20px; 
            }
            QListWidget::item {
                background-color: transparent;
                color: black;
                border: 2px solid black; 
                border-radius: 20px;
                padding-top: 10px
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

        self.fill()
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        
        for i in range(self.count()):
            item: QListWidgetItem = self.item(i)
            if self.visualItemRect(self.item(i)).contains(event.pos(), False):
                self.addProduit(item)
    
    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        
        for i in range(self.count()):
            item: QListWidgetItem = self.item(i)
            if self.visualItemRect(self.item(i)).contains(event.pos(), False):
                self.addProduit(item)

    def addProduit(self, item):
        self.produitClicked.emit(item.data(-1))
    
    def fill(self: QListProduits) -> None:
        #! TODO: dataclass pour les produits et donc retirer qt de la gestion des fichiers

        self.clear()
        for produit in self.list_produit:
            nom = produit.nom
            color = produit.color

            item = QListWidgetItem(self)
            item.setData(Qt.ItemDataRole.DisplayRole, nom)
            item.setData(-1, produit)
            colour = QColor(color)
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
