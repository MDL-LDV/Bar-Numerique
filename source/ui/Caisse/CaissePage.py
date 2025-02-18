from __future__ import annotations

from PySide6.QtWidgets import QWidget

from typing import Optional

from .QListProduits import QListProduits
from .QPaymentBar import QPaymentBar
from core import QRatioSlitter


class CaissePage(QRatioSlitter):
    def __init__(self: CaissePage, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("Caisse")
        self.setAllCollapsible(False)

        self.produits = QListProduits(self)
        self.addWidget(self.produits)
        
        self.payment = QPaymentBar(self)
        self.produits.produitClicked.connect(self.payment.addProduit)
        self.addWidget(self.payment)

        self.setSizes([4, 1])
        
        self.setMinimumWidth(
            self.produits.minimumWidth()
            + self.payment.minimumWidth()
            + self.handleWidth()
        )

        self.setMinimumHeight(
            max(
                self.produits.minimumHeight(),
                self.payment.minimumHeight()
            )
        )
    
    def resizeEvent(self, arg__1):
        return super().resizeEvent(arg__1)
