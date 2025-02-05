from PySide6.QtWidgets import QApplication
import sys
from ui.MainWindow import MainWindow


if __name__ == "__main__" and sys.version_info >= (3, 12):
    # Modifier les arguments pour forcer l'usage du mode clair
    # https://doc.qt.io/qt-6/qguiapplication.html#platform-specific-arguments
    sys.argv += ['-platform', 'windows:darkmode=0']

    # Déclaration de application
    application = QApplication(sys.argv)

    # Standardisation du style sur tous les OS
    application.setStyle("Fusion")
    # Définition du nom de l'application
    application.setApplicationName("Bar numérique")
    # Définition du nom de l'organisation de l'application
    application.setOrganizationName("Maison Des Lycéens")
    # Définition du nom de domain de l'application
    # application.setOrganizationDomain("")
    # Définition de la version de l'application (normalisé)
    # https://semver.org/spec/v2.0.0.html
    application.setApplicationVersion("v1.0.0-poc")

    # Instanciation de MainWindow, la fenêtre principale
    window = MainWindow(None)

    # On execute l'application
    sys.exit(application.exec())
