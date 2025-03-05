from pathlib import Path
from configparser import ConfigParser

def acquire(ConfigName: str, inipath: Path = "config.ini") -> object|None:
    """
    récupere une valeur de configuration 
    en priorisant si elle à été customisé via ["Custom"]

    parametre:
        ConfigName: str
            Nom de la valeur à chercher dans le fichier de configuration
        
        Dbpath: Path
            chemin d'accès au fichier de configuration
    retour 
        Object:
            la valeur à été trouvé et est retourné
        None:
            aucune valeur trouvé

    """
    parser = ConfigParser()
    parser.read(inipath)

    if (ConfigName in parser["Custom"]):
        return parser["Custom"][ConfigName]
    elif (ConfigName in parser["Default"]):
        return parser["Default"][ConfigName]
    else :
        return None
    
def checkConfig(listCheck: list[list[str, str]], inipath: Path = "config.ini") -> dict[str]:
    """
    recupere une list de valeur dans le fichier de configuration
    si la valeur est pas present, elle est remplace par une valeur 
    specifié

    parametre:
        listCheck: list[list[str, str]]
            list de valeur qui contient le nom de la valeur à chercher
            et la valeur si elle est pas trouvé
        Dbpath: Path
            chemin d'accès au fichier de configuration

    retour:
        dict[str]:
            dictionnaire avec comme clé le nom de la valeur à chercher
            et comme valeur celle trouve ou specifie
    """
    parser = ConfigParser()
    parser.read(inipath)
    retConfig: dict[str] = dict()
    for (configName, default) in listCheck:
            retConfig[configName] = conf if (conf := acquire(configName)) else default
    return retConfig