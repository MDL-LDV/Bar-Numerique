from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QLockFile
from ui.MainWindow import MainWindow
from pathlib import Path
from shutil import move, copy
import sys
import os


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

        #verifie si la db est toujours dans le strockage local de l'appli
        if (os.path.isfile(sys.path[0] + "\\commandes.sqlite3")):
            #migre la db dans path= %appdata%\Bar-Numerique
            appdata_path = os.getenv('APPDATA')
            
            if not os.path.exists(appdata_path + "\\Bar-Numerique\\commandes.sqlite3"):
                if os.path.isdir(appdata_path + "\\Bar-Numerique"):
                    copy(sys.path[0] + "\\commandes.sqlite3", (appdata_path + "\\Bar-Numerique\\commandes.sqlite3"))
                    print("The db as been moved to %AppData%\\Bar-Numerique\\commandes.sqlite3")
                else:
                    Path(appdata_path  +  "\\Bar-Numerique").mkdir(parents=True, exist_ok=True)
                    copy(sys.path[0] + "\\commandes.sqlite3", (appdata_path + "\\Bar-Numerique\\commandes.sqlite3"))
                    print("The db as been moved to %AppData%\\Bar-Numerique\\commandes.sqlite3")

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
        application.setApplicationVersion("v1.0.2-alpha")

        # Instanciation de MainWindow, la fenêtre principale
        window = MainWindow(None)

        # Ensure the lock is released when the application exits
        application.aboutToQuit.connect(lock_file.unlock)

        sys.exit(application.exec())
    else:
        QMessageBox.warning(None, "Error", "The application is already running!")
        sys.exit(1)
