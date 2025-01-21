from __future__ import annotations

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import QSize

from typing import Optional


class QFriendWidget(QWidget):
    def __init__(self: QFriendWidget, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._friend: QWidget = None

        self.central_layout = QHBoxLayout(self)
        bonjour = QLabel(self)
        bonjour.setText("AU revoir")
        self.central_layout.addWidget(bonjour)

        self.setContentsMargins(0, 0, 0, 0)
    
    def friend(self: QFriendWidget) -> QWidget | None:
        return self._friend
    
    def setFriend(self: QFriendWidget, friend: QWidget) -> None:
        # if isinstance(friend, QWidget):
        #     self._friend = friend
            
        # else:
        #     raise TypeError("Type asked: " + QWidget.__module__ + "."
        #                     + QWidget.__name__
        #                     + "\n\tTyped entered: " 
        #                     + friend.__class__.__module__ + "." 
        #                     + friend.__class__.__name__)
        self._friend = friend
    
    def resizeEvent(self, event):
        return super().resizeEvent(event)
