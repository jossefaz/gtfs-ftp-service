from utils.geometry import getJerusalemBorder, checkPointsFromFile, checkLinesFromFile
reg_controller = {
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
        }





    }
}
