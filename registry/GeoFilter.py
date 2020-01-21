from utils.geometry import getJerusalemBorder, checkPointsFromFile, checkLinesFromFile
from Controller.Feeder import Feeder
from Controller.AlphaFilter import AlphaFilter

REGISTRY = {
    "geometry" : {
        "line": checkLinesFromFile,
        "point": checkPointsFromFile
    },
    "AOI" : {
        "JERUSALEM" : getJerusalemBorder
    },
    "filter" : {
        "within" : "within",
        "outbound" : "outbound"
    },
    "callbacks" : {
        "feedData" : {
            "factory" : Feeder,
            "parameter" : "tables"
        },
        "filterAlphanum" : {
            "factory" : AlphaFilter,
            "parameter" : "tables"
        }

    }

}