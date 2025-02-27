from __future__ import annotations

from PySide6.QtWidgets import (QWidget, QFrame, QVBoxLayout, QLayout, QLabel, 
    QGridLayout, QPushButton, QSpacerItem, QSizePolicy, QScrollArea)
from PySide6.QtCore import (Signal, QSize, Qt)
from core.Produit import ProduitData
from core.core import enregistrer_commande, MethodesPayment
from decimal import Decimal
from PySide6.QtGui import QFontMetrics

from core.QtAddOns import QRatioSlitter


class EllipsisLabel(QLabel):
    """
    https://forum.qt.io/post/812856
    """
    def __init__(self, parent=None, text=""):
        super().__init__(parent)
        self._text = text
        self.setText(text)

    def setText(self, text):
        self._text = text
        self.updateText()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateText()
        # print("Ellipsis", self.width())

    def updateText(self):
        metrics = QFontMetrics(self.font())
        elided = metrics.elidedText(self._text, Qt.ElideRight, self.width() - 1)
        super().setText(elided)


class EntreeProduit(QFrame):
    removed = Signal(ProduitData)
    produitAdded = Signal(ProduitData)
    produitRemoved = Signal(ProduitData)
    def __init__(self, parent: QWidget, produit: ProduitData):
        super().__init__(parent)
        self.produit = produit
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
        # self.div.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self.nom_label = EllipsisLabel(self)
        self.nom_label.setText(self.produit.nom)
        self.div.addWidget(self.nom_label, 0, 0, Qt.AlignmentFlag.AlignBaseline)
        self.div.setColumnStretch(0, 7)

        self.nombre = 1

        self.minus_button = QPushButton(self)
        self.minus_button.setFixedSize(25, 25)
        self.minus_button.pressed.connect(self.decremente)
        self.minus_button.setText("-")
        self.minus_button.adjustSize()
        self.div.addWidget(self.minus_button, 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.div.setColumnStretch(3, 1)

        self.quantite_label = QLabel(self)
        self.quantite_label.setText(str(self.nombre))
        self.quantite_label.adjustSize()
        self.div.addWidget(self.quantite_label, 0, 2, Qt.AlignmentFlag.AlignCenter)
        self.div.setColumnStretch(2, 1)

        self.plus_button = QPushButton(self)
        self.plus_button.setFixedSize(25, 25)
        self.plus_button.pressed.connect(self.incremente)
        self.plus_button.setText("+")
        self.plus_button.adjustSize()
        self.div.addWidget(self.plus_button, 0, 3, Qt.AlignmentFlag.AlignCenter)
        self.div.setColumnStretch(1, 1)

        self.setMinimumWidth(200)
        self.setFixedHeight(45)

        # print("Div", self.div.totalMinimumSize())

        self.setLayout(self.div)
    
    def resizeEvent(self, event):
        # print("EProduit", event, "\n")
        return super().resizeEvent(event)
    
    def setProduit(self: EntreeProduit, produit: ProduitData) -> None:
        self.produit = produit
        self.nom_label.setText(self.produit.nom)
    
    def incremente(self: EntreeProduit):
        self.produitAdded.emit(self.produit)
        self.nombre += 1
        self.quantite_label.setText(str(self.nombre))

    def decremente(self: EntreeProduit):
        self.produitRemoved.emit(self.produit)
        if self.nombre <= 1:
            self.removed.emit(self.produit)
        
        self.nombre -= 1
        self.quantite_label.setText(str(self.nombre))
    
    def minimumSizeHint(self):
        # return super().minimumSizeHint()
        return self.minimumSize()


class Panier(QScrollArea):
    produitAdded = Signal(ProduitData)
    produitRemoved = Signal(ProduitData)
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        
        self.widget_central = QWidget(self)
        self.setWidget(self.widget_central)

        self.liste = QVBoxLayout(self)
        self.widget_central.setLayout(self.liste)

        self.liste.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.liste_produits: dict[ProduitData: EntreeProduit] = {}

        self.setMinimumWidth(
            # EntreeProduit.minimumWidth()
            200
            + self.liste.contentsMargins().left() 
            + self.liste.contentsMargins().right()
            + self.verticalScrollBar().width()
            + 1
        )

        self.setMinimumHeight(
            self.liste.contentsMargins().top()
            # EntreeProduit.minimumHeight()
            + 45
            + self.liste.spacing()
            + self.liste.contentsMargins().bottom()
        )

        self.iterator = 0
    
    def sizeHint(self):
        # return super().sizeHint()
        return QSize(0, 0)

    def minimumSizeHint(self):
        # return super().minimumSizeHint()
        return QSize(0, 0)
    
    def addProduit(self, produit: ProduitData):
        if produit in self.liste_produits:
            self.liste_produits[produit].incremente()
        else:
            self.produitAdded.emit(produit)
            widget = EntreeProduit(self, produit)
            widget.removed.connect(self.removeProduit)
            widget.produitAdded.connect(lambda p: self.produitAdded.emit(p))
            widget.produitRemoved.connect(lambda p: self.produitRemoved.emit(p))
            self.liste.addWidget(widget)
            self.liste_produits[produit] = widget
    
    def removeProduit(self: Panier, produit: ProduitData) -> None:
        self.liste.removeWidget(self.liste_produits[produit])

        self.liste_produits[produit].hide()
        self.liste_produits[produit].deleteLater()
        self.liste_produits.__delitem__(produit)
    
    def clear(self: Panier) -> None:
        for produit in self.liste_produits.copy():
            self.removeProduit(produit)


class Payment(QWidget):
    def __init__(self: Payment, parent: QWidget, panier: Panier):
        super().__init__(parent)
        self.liste_produits: list[ProduitData] = []
        self.prix_total: Decimal = Decimal("0.00")
        self.panier = panier
        self.setStyleSheet(
            """QLabel { 
                font-size: 25px; 
            }
            QPushButton {
                font-size: 18px;
                border: 1px solid black;
                border-radius: 10px;
                background-color: #CDD0DA;
            }
            QPushButton:pressed {
                background-color: #8A91A8;
            }
            """
        )

        self.div = QGridLayout(self)
        self.div.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.div.setSpacing(0)

        self.total_label = QLabel(self)
        self.total_label.setText("Total")
        self.total_label.adjustSize()
        self.div.addWidget(self.total_label, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.prix_label = QLabel(self)
        self.update_prix()
        self.prix_label.adjustSize()
        self.div.addWidget(self.prix_label, 0, 2, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        self.cash_button = QPushButton(self)
        self.cash_button.setFixedSize(120, 70)
        self.cash_button.pressed.connect(lambda: self.encaisser(MethodesPayment.Cash))
        self.cash_button.setText("Espèces")
        self.cash_button.adjustSize()
        self.div.addWidget(self.cash_button, 1, 0, Qt.AlignmentFlag.AlignCenter)

        spacer = QSpacerItem(5, 0, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Ignored)
        self.div.addItem(spacer, 1, 1)

        self.carte_button = QPushButton(self)
        self.carte_button.setFixedSize(120, 70)
        self.carte_button.pressed.connect(lambda: self.encaisser(MethodesPayment.CB))
        self.carte_button.setText("Carte")
        self.carte_button.adjustSize()
        self.div.addWidget(self.carte_button, 1, 2, Qt.AlignmentFlag.AlignCenter)

        self.setMinimumSize(self.div.totalMinimumSize())
    
    def encaisser(self: Payment, methode: MethodesPayment) -> None:
        if self.panier.liste_produits:
            prix = Decimal()
            produit_nombre: dict[ProduitData: int] = {}
            for produit in self.panier.liste_produits:
                prix += self.panier.liste_produits[produit].nombre * produit.prix
                produit_nombre[produit] = self.panier.liste_produits[produit].nombre
            
            enregistrer_commande(methode, prix, produit_nombre)
            self.panier.clear()
            self.clear_prix()
    
    def sizeHint(self: Payment):
        # return super().sizeHint()
        return QSize(0, 0)

    def minimumSizeHint(self: Payment):
        # return super().minimumSizeHint()
        return QSize(0, 0)
    
    def update_prix(self: Payment):
        self.prix_label.setText("{:.02f} €".format(self.prix_total))
    
    def clear_prix(self: Payment):
        self.prix_total -= self.prix_total
        self.update_prix()

    def addProduit(self: Payment, produit: ProduitData):
        self.liste_produits.append(produit)
        self.prix_total += produit.prix
        self.update_prix()
    
    def removeProduit(self: Payment, produit: ProduitData) -> None:
        self.liste_produits.remove(produit)
        self.prix_total -= produit.prix
        self.update_prix()


class QPaymentBar(QRatioSlitter):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setOrientation(Qt.Orientation.Vertical)
        self.setStyleSheet("QSplitter:handle { border-bottom: 1px solid black }")
        self.setAllCollapsible(False)

        self.panier = Panier(self)
        self.addWidget(self.panier)

        self.payment = Payment(self, self.panier)
        self.panier.produitAdded.connect(self.payment.addProduit)
        self.panier.produitRemoved.connect(self.payment.removeProduit)
        self.addWidget(self.payment)

        self.setSizes([7, 2])
        
        self.setMinimumWidth(
            max(self.panier.minimumWidth(), self.payment.minimumWidth())
        )

        self.setMinimumHeight(
            self.panier.minimumHeight()
            + self.handleWidth()
            + self.payment.minimumHeight()
        )
    
    def resizeEvent(self, event):
        # print("Splitter", event)
        
        # handleWidth = self.handleWidth()
        # self.setHandleWidth(0)
        # super().resizeEvent(event)
        # self.setHandleWidth(handleWidth)
        
        super().resizeEvent(event)
    
    def addProduit(self, produit: ProduitData):
        self.panier.addProduit(produit)
    
    def minimumSizeHint(self):
        # return super().minimumSizeHint()
        return self.minimumSize()
