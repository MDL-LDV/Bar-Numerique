from pathlib import Path
from configparser import ConfigParser

def acquire(ConfigName: str, Dbpath: Path = "config.ini") -> object:
    parser = ConfigParser()
    parser.read(Dbpath)

    if (ConfigName in parser["Custom"]):
        return parser["Custom"][ConfigName]
    elif (ConfigName in parser["Default"]):
        return parser["Default"][ConfigName]
    else :
        return None
    
def checkConfig(listCheck: list[list[str]], Dbpath: Path = "config.ini") -> dict[str]:
    parser = ConfigParser()
    parser.read(Dbpath)
    retConfig: dict[str] = dict()
    for (configName, default) in listCheck:
            retConfig[configName] = conf if (conf := acquire(configName)) else default
    return retConfig