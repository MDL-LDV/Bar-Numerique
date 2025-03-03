from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QLockFile
import sys
from ui.MainWindow import MainWindow


if __name__ == "__main__" and sys.version_info >= (3, 12):
    # Modifier les arguments pour forcer l'usage du mode clair
    # https://doc.qt.io/qt-6/qguiapplication.html#platform-specific-arguments
    sys.argv += ['-platform', 'windows:darkmode=0']
    
    # Déclaration de application
    application = QApplication(sys.argv)

    #creer un fichier lock
    #sert à s'assurer qu'une instance de l'appli est démarer
    lock_file = QLockFile("app.lock")
    if lock_file.tryLock(100):
        # Proceed with your application
        print("Starting the application.")
        # Your application code here

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

        # Ensure the lock is released when the application exits
        application.aboutToQuit.connect(lock_file.unlock)

        sys.exit(application.exec_())
    else:
        QMessageBox.warning(None, "Error", "The application is already running!")
        sys.exit(1)

        

    
    

