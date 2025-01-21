from __future__ import annotations
from PySide6.QtWidgets import QWidget, QListWidget, QListWidgetItem
from core.QtAddOns import QFriendWidget

from core.QtAddOns import QListWidgetItemId

# from typing import Optional


class QNavigationBar(QWidget):
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
        self.onglets.setStyleSheet("background-color: green;")
        self.onglets.itemPressed.connect(self.dispatcher)
        self.map_index_call: dict[QListWidgetItemId: callable] = {}

    def addItem(self: QNavigationBar, item: QListWidgetItemId, f: callable)\
            -> None:
        if isinstance(item, QListWidgetItemId):
            self.onglets.addItem(item)
            self.map_index_call[item] = f
        else:
            raise TypeError("Type asked: " + QListWidgetItemId.__module__ + "."
                            + QListWidgetItemId.__name__
                            + "\n\tTyped entered: " 
                            + item.__class__.__module__ + "." 
                            + item.__class__.__name__)
    
    def addWidget(self: QNavigationBar, widget: QFriendWidget) -> None:
        if isinstance(widget, QWidget):
            item = QListWidgetItemId()
            widget.setFriend(item)
            self.onglets.setItemWidget(item, widget)
        else:
            pass
    
    def removeItem(self: QNavigationBar, item: QListWidgetItemId) -> None:
        if item in self.onglets.items():
            self.map_index_call.pop(item)
            self.onglets.removeItemWidget(item)
        else:
            raise IndexError(
                f"L'élément {item} n'est pas dans {self.__class__.__name__}#"
                + f"{self.objectName()}, il ne peut donc pas en être retiré"
            )
    
    def dispatcher(self, item: QListWidgetItemId) -> None:
        self.map_index_call[item].__call__()
    
    def resizeEvent(self, event):
        self.onglets.resize(event.size())
        return super().resizeEvent(event)
