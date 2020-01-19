from utils.geometry import getJerusalemBorder
reg_controller = {
    "GeoFilter" : {
        "geometry" : {
            "line": "checkLinesFromFile",
            "point": "checkPointsFromFile"
        },
        "filters" : {
            "JERUSALEM" : getJerusalemBorder
        }


    }
}
