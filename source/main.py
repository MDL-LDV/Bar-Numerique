from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QProcess
import sys
from ui.MainWindow import MainWindow


if __name__ == "__main__" and sys.version_info >= (3, 12):
    # https://doc.qt.io/qt-6/qguiapplication.html#platform-specific-arguments
    sys.argv += ['-platform', 'windows:darkmode=0']

    application = QApplication(sys.argv)
    # hope it works
    # windows11 sur Windows 11 donc Fusion sur tous les OS
    application.setStyle("Fusion")

    application.setApplicationName("Bar numérique")
    application.setOrganizationName("Maison Des Lycéens")
    # application.setOrganizationDomain("")
    application.setApplicationVersion("Alpha")

    window = MainWindow(None)

    sys.exit(application.exec())
