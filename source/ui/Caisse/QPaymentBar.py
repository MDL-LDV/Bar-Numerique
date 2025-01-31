from __future__ import annotations

from PySide6.QtWidgets import (QWidget, QFrame, QVBoxLayout, QLabel, QSplitter, 
    QGridLayout, QPushButton)
from PySide6.QtCore import (Signal, QSize, Qt)
from core.Produit import ProduitData

from typing import Optional


class EntreeProduit(QFrame):
    removed = Signal(ProduitData)
    def __init__(self, parent: QWidget, produit: Optional[ProduitData] = None):
        super().__init__(parent)
        self.setStyleSheet(
            """
            QFrame { 
                border: 1px solid black; 
                border-radius: 5px;
            } 
            QLabel { 
                color: black; 
                border: none; 
                font-size: 18px; 
            } 
            QPushButton { 
                padding-bottom: 5px; 
                font-size: 25px; 
                background-color: #CDD0DA;  
                border-radius: 3px;
            }""")
        self.div = QGridLayout(self)

        self.nom_label = QLabel(self)
        self.produit = produit
        if self.produit:
            print(self.produit.nom)
            self.nom_label.setText(self.produit.nom)
        self.div.addWidget(self.nom_label, 0, 0, Qt.AlignmentFlag.AlignBaseline)
        self.div.setColumnStretch(0, 7)

        self.nombre = 1

        self.plus_button = QPushButton(self)
        self.plus_button.setFixedSize(25, 25)
        self.plus_button.pressed.connect(self.incremente)
        self.plus_button.setText("+")
        self.plus_button.adjustSize()
        self.div.addWidget(self.plus_button, 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.div.setColumnStretch(1, 1)

        self.quantite_label = QLabel(self)
        self.quantite_label.setText(str(self.nombre))
        self.quantite_label.adjustSize()
        self.div.addWidget(self.quantite_label, 0, 2, Qt.AlignmentFlag.AlignCenter)
        self.div.setColumnStretch(2, 1)

        self.minus_button = QPushButton(self)
        self.minus_button.setFixedSize(25, 25)
        self.minus_button.pressed.connect(self.decremente)
        self.minus_button.setText("-")
        self.minus_button.adjustSize()
        self.div.addWidget(self.minus_button, 0, 3, Qt.AlignmentFlag.AlignCenter)
        self.div.setColumnStretch(3, 1)

        self.setLayout(self.div)
    
    def setProduit(self: EntreeProduit, produit: ProduitData) -> None:
        self.produit = produit
        self.nom_label.setText(self.produit.nom)
    
    def incremente(self: EntreeProduit):
        self.nombre += 1
        self.quantite_label.setText(str(self.nombre))

    def decremente(self: EntreeProduit):
        if self.nombre <= 1:
            self.removed.emit(self.produit)
        
        self.nombre -= 1
        self.quantite_label.setText(str(self.nombre))


class Panier(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setStyleSheet("padding: 0px;")
        self.liste = QVBoxLayout(self)
        self.liste.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.liste_produits: dict[ProduitData: QWidget] = {}
    
    def minimumSizeHint(self):
        # return super().minimumSizeHint()
        return QSize(0, 0)
    
    def addProduit(self, produit: ProduitData):
        print(produit)

        if produit in self.liste_produits:
            pass
        else:
            # widget = QWidget(self)
            # widget.setStyleSheet("border: 1px solid black; border-radius: 5px; color: black;")
            # widget.setFixedHeight(50)
            # l = QHBoxLayout(widget)
            # text = QLabel(widget)
            # l.addWidget(text)
            # text.setStyleSheet("border: none;")
            # text.setText(produit.nom)
            # qu = QLabel(widget)
            # qu.setStyleSheet("border: none;")
            # qu.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            # l.addWidget(qu)
            # qu.setText("1")
            widget = EntreeProduit(self, produit)
            widget.removed.connect(self.removeProduit)
            self.liste.addWidget(widget)
            self.liste_produits[produit] = widget
    
    def removeProduit(self: Panier, produit: ProduitData) -> None:
        self.liste.removeWidget(self.liste_produits[produit])

        self.liste_produits[produit].hide()
        self.liste_produits[produit].deleteLater()
        self.liste_produits.__delitem__(produit)


class QPaymentBar(QSplitter):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setOrientation(Qt.Orientation.Vertical)
        self.panier = Panier(self)

        self.addWidget(self.panier)
        self.payment = QWidget(self)
        self.payment.setStyleSheet("background-color: yellow;")
        self.addWidget(self.payment)

        self.setSizes([4, 1])
    
    def addProduit(self, produit: ProduitData):
        self.panier.addProduit(produit)
    
    def resizeEvent(self, event):
        return super().resizeEvent(event)
    
    def sizeHint(self):
        # return super().sizeHint()
        return QSize(0, 0)

    def minimumSizeHint(self):
        # return super().minimumSizeHint()
        return QSize(0, 0)        
