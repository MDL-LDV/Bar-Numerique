from __future__ import annotations

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import QSize

from typing import Optional


class CaissePage(QWidget):
    def __init__(self: CaissePage, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("Caisse")
        self.setStyleSheet("QWidget { background-color: white; border: 2px solid black; }")

        self.central_layout = QHBoxLayout(self)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        bonjour = QLabel("Bonjour", self)
        self.central_layout.addWidget(bonjour)
