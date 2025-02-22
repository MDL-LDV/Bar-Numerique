from __future__ import annotations

from PySide6.QtWidgets import QWidget, QFrame

class Commande(QFrame):
    def __init__(self: Commande, parent: QWidget) -> None:
        super().__init__(parent)

class ListeCommandes(QFrame):
    def __init__(self: ListeCommandes, parent: QWidget) -> None:
        super().__init__(parent)


class HistoriquePage(QFrame):
    def __init__(self: HistoriquePage, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("Historique")
        
        self.setStyleSheet("background-color: yellow;")
