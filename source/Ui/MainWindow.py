from PySide6.QtWidgets import QMainWindow, QWidget

from typing import Optional

from sys import version
from ctypes import windll


class MainWindow(QMainWindow):
    """
    Parent:
        QMainWindow
    Role:
        pass
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Inputs:
            parent: Optional[QWidget]
                default: None
        Outputs:
            None (ctor)
        """
        super().__init__(parent)

        # Give the app a name
        self.setWindowTitle("Bar numérique")

        # Définit l'icone dans la bar des tâches (en utilisant celle de 
        # l'application) https://stackoverflow.com/a/1552105/15793884
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            f"{self.windowTitle()}_{version}"
        )

        self.show()


