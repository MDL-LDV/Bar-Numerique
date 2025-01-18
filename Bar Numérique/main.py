from PySide6.QtWidgets import QApplication
import sys
from Ui.MainWindow import MainWindow


if __name__ == "__main__" and sys.version_info >= (3, 12):
    application = QApplication()

    window = MainWindow(None)

    sys.exit(application.exec())
