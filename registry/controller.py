from utils.geometry import getJerusalemBorder, checkPointsFromFile, checkLinesFromFile
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
            "feedData" : "feedData"
        }

    },
    "Feeder" : {
        "callbacks" : {
            "concatenate_field" : "concatenate_field"
        }
    }

}
