from __future__ import annotations

from PySide6.QtWidgets import QListWidgetItem, QListWidget

from typing import Optional, Any

class QListWidgetItemId(QListWidgetItem):
    """
    Héritage:
    Rôle:
    """

    def __init__(self: QListWidgetItemId, 
                 listview: Optional[QListWidget] = None) -> None:
        """
        Entrées:
            self: QListWidgetItemId
            listview: QListWidget
                optional
                default: None
        Sortie:
            None (ctor)
        Rôle:
        """
        super().__init__(listview)
    
    def __hash__(self: QListWidgetItemId) -> int:
        """
        Entrée:
            self: QListWidgetItemId
        Sortie:
            int
        Rôle:
            Hash QListWidgetItemId pour qu'il puisse être utilisé dans un 
            mapping.
        """
        # WARNING: Two objects that compare equal must also have the same hash 
        # value, but the reverse is not necessarily true.
        return hash(id(self))
    
    def __eq__(self: QListWidgetItemId, valeur: Any) -> bool:
        """
        Entrées:
            self: QListWidgetItemId
            valeur: Any
        Sortie:
            bool (comparaison)
        Rôle:
            Retourne 
        """
        # WARNING: Two objects that compare equal must also have the same hash 
        # value, but the reverse is not necessarily true.
        return False
