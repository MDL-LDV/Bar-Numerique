from __future__ import annotations
from PySide6.QtWidgets import QWidget, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, QEvent, Signal

from core.QtAddOns import QListWidgetItemId

# from typing import Optional


class QNavigationBar(QWidget):
    pageclicked = Signal(str)

    def __init__(self: QNavigationBar, parent: QWidget) -> None:
        """
        Entrées:
            self: QNavigationBar
            parent: QWidget
        Sortie:
            None (ctor)
        Rôle:
            Ctor
        """
        super().__init__(parent)

        self.onglets = QListWidget(self)
        self.onglets.setSpacing(5)
        self.onglets.setStyleSheet(
            """
            QListWidget { 
                border-right: 1px solid #000000;
            }
            QListWidget::item {
                border: 1px solid black;
                border-radius: 10px;
                font-size: 20px;
                width: 100%;
                height: 150px;
            }
            QListWidget::item:selected {
                background-color: rgba(135, 190, 255, 50);
                color: black;
            }
            """)
        self.onglets.itemPressed.connect(self.dispatcher)
        # self.map_index_call: dict[QListWidgetItemId: callable] = {}

    def addItem(self: QNavigationBar, item: QListWidgetItemId, f: callable | None = None)\
            -> None:
        if isinstance(item, QListWidgetItemId):
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.onglets.addItem(item)
            # TODO check f's type
            # self.map_index_call[item] = f
        else:
            raise TypeError("Type asked: " + QListWidgetItemId.__module__ + "."
                            + QListWidgetItemId.__name__
                            + "\n\tTyped entered: " 
                            + item.__class__.__module__ + "." 
                            + item.__class__.__name__)
    
    def addWidget(self: QNavigationBar, widget: QWidget, f: callable)\
            -> None:
        if isinstance(widget, QWidget):
            item = QListWidgetItemId(self.onglets)
            item.setSizeHint(widget.minimumSizeHint())
            self.onglets.setItemWidget(item, widget)
            # TODO check f's type
            # self.map_index_call[item] = f
        else:
            raise TypeError("Type asked: " + QWidget.__module__ + "."
                            + QWidget.__name__
                            + "\n\tTyped entered: " 
                            + widget.__class__.__module__ + "." 
                            + widget.__class__.__name__)
    
    def removeItem(self: QNavigationBar, item: QListWidgetItemId) -> None:
        if item in self.onglets.items():
            # self.map_index_call.pop(item)
            self.onglets.removeItemWidget(item)
        else:
            raise IndexError(
                f"L'élément {item} n'est pas dans {self.__class__.__name__}#"
                + f"{self.objectName()}, il ne peut donc pas en être retiré"
            )
    
    def dispatcher(self: QNavigationBar, item: QListWidgetItemId) -> None:
        # self.map_index_call[item].__call__()
        self.pageclicked.emit(item.identifiant)
    
    def resizeEvent(self: QNavigationBar, event: QEvent) -> None:
        self.onglets.resize(event.size())
        return super().resizeEvent(event)
    
    def activer(self: QNavigationBar) -> None:
        if self.isHidden():
            self.show()
        else:
            self.hide()
        
        self.update()
