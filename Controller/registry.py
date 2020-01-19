from utils.geometry import getJerusalemBorder, checkPointsFromFile, checkLinesFromFile
reg_controller = {
    "GeoFilter" : {
        "geometry" : {
            "line": checkLinesFromFile,
            "point": checkPointsFromFile
        },
        "geoMask" : {
            "JERUSALEM" : getJerusalemBorder
        },
        "geoAction" : {
            "within" : "within",
            "outbound" : "outbound"
        }





    }
}
