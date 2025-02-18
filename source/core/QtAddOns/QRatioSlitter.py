from __future__ import annotations

from PySide6.QtWidgets import QApplication, QSplitter, QWidget

class QRatioSlitter(QSplitter):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        
        app: QApplication = QApplication.instance()
        self.max_screen_width = max(
            [screen.virtualSize().width() for screen in app.screens()]
        )
        self.defaultCollapsibleBehavior = True
    
    def addWidget(self, widget):
        super().addWidget(widget)
        index = self.indexOf(widget)
        self.setCollapsible(index, self.defaultCollapsibleBehavior)

    def setAllCollapsible(self, collapsible: bool):
        self.defaultCollapsibleBehavior = collapsible
        for i in range(self.count()):
            self.setCollapsible(i, collapsible)
    
    def setSizes(self, sizes: list):
        # https://stackoverflow.com/a/35166717
        return super().setSizes([i * self.max_screen_width for i in sizes])
