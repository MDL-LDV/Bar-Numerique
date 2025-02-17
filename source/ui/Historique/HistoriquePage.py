from __future__ import annotations

from PySide6.QtWidgets import QWidget, QFrame

from typing import Optional


class HistoriquePage(QFrame):
    def __init__(self: HistoriquePage, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("Historique")
        
        self.setStyleSheet("background-color: yellow;")
