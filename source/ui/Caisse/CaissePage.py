from __future__ import annotations

from PySide6.QtWidgets import QWidget, QSplitter

from typing import Optional

from .QListProduits import QListProduits
from .QPaymentBar import QPaymentBar


class CaissePage(QSplitter):
    def __init__(self: CaissePage, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("Caisse")

        self.produits = QListProduits(self)
        self.addWidget(self.produits)
        
        self.payment = QPaymentBar(self)
        self.produits.produitClicked.connect(self.payment.addProduit)
        self.addWidget(self.payment)

        self.setSizes([7, 2])
