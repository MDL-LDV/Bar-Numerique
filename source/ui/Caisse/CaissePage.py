from __future__ import annotations

from PySide6.QtWidgets import QWidget, QSplitter

from typing import Optional

from .QListProduits import QListProduits


class CaissePage(QSplitter):
    def __init__(self: CaissePage, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("Caisse")

        self.produits = QListProduits(self)
        self.addWidget(self.produits)
        
        self.payment = QWidget()
        self.payment.setStyleSheet("background-color: yellow;")
        self.addWidget(self.payment)

        self.setSizes([4, 1])
