from PySide6.QtWidgets import (QListWidget, QWidget, QListView, 
    QListWidgetItem, QLabel, QStyledItemDelegate, QStyleOptionViewItem, QStyle, 
    QSplitter)
from PySide6.QtGui import QMouseEvent, QColor, QPainter
from PySide6.QtCore import (QFileInfo, QDir, QJsonDocument, QJsonArray, 
    QJsonValue, QSize, Qt, QModelIndex, QPersistentModelIndex)
from core.core import Core
from core.Produit import ProduitData, ListeProduits

class Panier(QListWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.liste_produits: list[ProduitData] = []
    
    def minimumSizeHint(self):
        # return super().minimumSizeHint()
        return QSize(0, 0)
    
    def addProduit(self, produit: ProduitData):
        if produit in self.liste_produits:
            pass
        else:
            item = QListWidgetItem(produit.nom)
            print(produit)
            self.addItem(item)


class QPaymentBar(QSplitter):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setStyleSheet("background-color: red;")
        self.setOrientation(Qt.Orientation.Vertical)
        self.panier = Panier(self)

        self.addWidget(self.panier)
        self.payment = QWidget(self)
        self.payment.setStyleSheet("background-color: yellow;")
        self.addWidget(self.payment)

        self.setSizes([4, 1])
    
    def addProduit(self, produit: ProduitData):
        print(produit)
        self.panier.addProduit(produit)
    
    def resizeEvent(self, event):
        return super().resizeEvent(event)
    
    def sizeHint(self):
        # return super().sizeHint()
        return QSize(0, 0)

    def minimumSizeHint(self):
        # return super().minimumSizeHint()
        return QSize(0, 0)        
