from __future__ import annotations

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout

from typing import Optional


class CaissePage(QWidget):
    def __init__(self: CaissePage, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("Caisse")
        self.setStyleSheet("QWidget { background-color: red; }")
        layout = QHBoxLayout(self)
        bonjour = QLabel("Bonjour", self)
        layout.addWidget(bonjour)
        self.setLayout(layout)