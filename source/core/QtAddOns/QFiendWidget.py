from __future__ import annotations

from PySide6.QtWidgets import QWidget

from typing import Optional


class QFriendWidget(QWidget):
    def __init__(self: QFriendWidget, parent: Optional[QWidget]):
        super().__init__(parent)
        self._friend: QWidget = None
    
    def friend(self: QFriendWidget) -> QWidget | None:
        return self._friend
    
    def setFriend(self: QFriendWidget, friend: QWidget) -> None:
        if isinstance(friend, QWidget):
            self._friend = friend
            
        else:
            raise TypeError("Type asked: " + QWidget.__module__ + "."
                            + QWidget.__name__
                            + "\n\tTyped entered: " 
                            + friend.__class__.__module__ + "." 
                            + friend.__class__.__name__)
    
    def resizeEvent(self, event):
        self._friend.resize(ev)
        return super().resizeEvent(event)
