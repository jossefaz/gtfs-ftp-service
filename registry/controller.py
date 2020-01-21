from utils.geometry import getJerusalemBorder, checkPointsFromFile, checkLinesFromFile
from Controller.Feeder import Feeder
from Controller.AlphaFilter import AlphaFilter
registry = {
    "GeoFilter" : {
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

    },
    "Feeder" : {
        "callbacks" : {
            "concatenate_field" : "concatenate_field"
        }
    },
    "AlphaFiler": {
        "filter": {
            "by_id": "by_id",
            "by_sql" : "by_sql"
        },
        "callbacks": {
            "concatenate_field": "concatenate_field"
        }
    }

}
