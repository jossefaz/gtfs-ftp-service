from utils.geometry import getJerusalemBorder, checkPointsFromFile, checkLinesFromFile
from Controller.Feeder import Feeder
from Controller.AlphaFilter import AlphaFilter
from Model.DAO import DAO
from utils.dummy import printFoo
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
        "feedData" :  Feeder,
        "filterAlphanum" : AlphaFilter,
        "printFoo" : printFoo,
        "DB" : DAO
        }

    }

