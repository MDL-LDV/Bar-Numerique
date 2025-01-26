from __future__ import annotations

from PySide6.QtWidgets import QStackedWidget, QWidget
from PySide6.QtCore import QSize

from typing import Optional


class QBody(QStackedWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.map_page_index: dict[str, int] = {}
    
    def addWidget(self, w: QWidget) -> int:
        if w.objectName():
            index = super().addWidget(w)
            self.map_page_index[w.objectName()] = index
            return index
        else:
            print("Le widget doit avoir un nom")
    
    def dispatcher(self: QBody, page: str) -> None:
        if page in self.map_page_index:
            self.setCurrentIndex(self.map_page_index[page])
            print(self.currentIndex(), self.currentWidget())
        else:
            print(f"La page ``{page}`` n'existe pas")
    
    def sizeHint(self):
        # return super().sizeHint()
        return QSize(-1, -1)

    def minimumSizeHint(self):
        # return super().minimumSizeHint()
        return QSize(-1, -1)
