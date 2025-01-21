from __future__ import annotations
from PySide6.QtWidgets import QListWidgetItem, QListWidget
from PySide6.QtCore import Qt

from typing import Optional

class QListWidgetItemId(QListWidgetItem):
    """
    Héritage:
    Rôle:
    """
    # Déclaration de static_index, qui est utilisé comme une variable statique 
    # en c++
    static_index = 0

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

        # Allocation automatique de l'indice (static en c++)
        # La variable est déclarée comme 'protected' grâce à l'underscore 
        # (convention de nommage uniquement)
        # https://tutorialsteacher.com/python/public-private-protected-modifiers
        self._identifiant = None

        self.est_espaceur: bool = False
    
    def setSpacer(self: QListWidgetItemId) -> None:
        """
        Entrée:
            self: QListWidgetItemId
        Sortie:
            None (modification en place)
        Rôle:
            Définit le rôle de l'objet comme spacer (espaceur).
        """
        if not self.est_espaceur:
            self.est_espaceur = True
            # On désactive l'item car il ne doit pas pouvoir être selectionné
            self.setFlags(self.flags() & ~Qt.ItemFlag.ItemIsEnabled)

    @property
    def identifiant(self: QListWidgetItemId) -> int:
        """
        Entrée:
            self: QListWidgetItemId
        Sortie:
            int
        Rôle:
            Getter de la propriété identifiant. Procure une interface abstraite 
            de communication avec la propriété indice pour en contrôler l'accès
            et l'écriture.
        """
        if self.est_espaceur:
            raise TypeError(
                f"The {self.__class__.__name__} does not support the "
                 + "'identifiant' propery getter, because it has been set to "
                 + "spacer.")
        else:
            # Retourne la valeur de la variable protégée identifiant
            return self._identifiant

    @identifiant.setter
    def identifiant(self: QListWidgetItemId, valeur: int) -> None:
        """"
        Entrées:
            self: QListWidgetItemId
            valeur: int
        Sortie:
            None (modification en place)
             | TypeError (indice est immuable)
        Rôle:
            Setter de la propriété identifiant. Procure une interface abstraite 
            de communication avec la propriété indice pour en contrôler l'accès
            et l'écriture.
        """
        if self._identifiant is None and not self.est_espaceur:
            self._identifiant = valeur
        elif self.est_espaceur:
            raise TypeError(
                f"The {self.__class__.__name__} does not support 'identifiant'"
                + " propery access, because it has been set to spacer.")
        else:
            raise TypeError(f"The {self.__class__.__name__} 'identifiant' "
                            + "propery does not support item assignment.")
    
    def __hash__(self) -> int:
        # TODO : change it and make it works
        return hash(str(self._identifiant))
    
    def __eq__(self, value) -> bool:
        return False
