from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QLockFile
from ui.MainWindow import MainWindow
from pathlib import Path
from shutil import copy
from getConfig import checkConfig
from core.Logger import BarLogger
import sys
import os


if __name__ == "__main__" and sys.version_info >= (3, 12):
    # Modifier les arguments pour forcer l'usage du mode clair
    # https://doc.qt.io/qt-6/qguiapplication.html#platform-specific-arguments
    sys.argv += ['-platform', 'windows:darkmode=0']
    
    # Déclaration de application
    application = QApplication(sys.argv)

    #recupere la configuation dans config.ini
    #en specifiant les valeurs à trouver et la value 
    #si la valeur est pas configurée
    config = checkConfig(list((
        list(("Version", "1.0.0")), 
        list(("OrgaName", "Maison Des Lycéens")),
        list(("AppName", "Bar numérique")),
        list(("QTheme", "Fusion")),
        list(("LogLevel", "INFO"))
    )))

    if (config["LogLevel"].isdigit() and ((int(config["LogLevel"]) % 10) == 0)):
        logger = BarLogger("MainLogger", int(config["LogLevel"]))
    else:
        logger = BarLogger("MainLogger", 20)#20 revient à logging.INFO

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
        logger.info("Starting the application.")
        # Your application code here

        # Standardisation du style sur tous les OS
        application.setStyle("Fusion")
        # Définition du nom de l'application
        application.setApplicationName(config["AppName"])
        # Définition du nom de l'organisation de l'application
        application.setOrganizationName(config["OrgaName"])
        # Définition du nom de domain de l'application
        # application.setOrganizationDomain("") 
        # Définition de la version de l'application (normalisé)
        # https://semver.org/spec/v2.0.0.html
        application.setApplicationVersion(config["Version"])

        # Instanciation de MainWindow, la fenêtre principale
        window = MainWindow(None)

        # Ensure the lock is released when the application exits
        application.aboutToQuit.connect(lock_file.unlock)
        application.aboutToQuit.connect(lambda:logger.info("Closing the application."))

        sys.exit(application.exec())
    else:
        QMessageBox.warning(None, "Error", "The application is already running!")
        sys.exit(1)
