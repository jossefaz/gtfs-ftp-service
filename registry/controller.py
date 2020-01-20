from utils.geometry import getJerusalemBorder, checkPointsFromFile, checkLinesFromFile
from Controller.Feeder import Feeder
registry = {
    "GeoFilter" : {
        "geometry" : {
            "line": checkLinesFromFile,
            "point": checkPointsFromFile
        },
        "AOI" : {
            "JERUSALEM" : getJerusalemBorder
        },
        "geoAction" : {
            "within" : "within",
            "outbound" : "outbound"
        },
        "callbacks" : {
            "feedData" : Feeder
        }

    },
    "Feeder" : {
        "callbacks" : {
            "concatenate_field" : "concatenate_field"
        }
    }

}
