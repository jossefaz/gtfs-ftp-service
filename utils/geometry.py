import csv
from functools import partial
import pyproj
from shapely.ops import transform

import shapely.wkt
def chechPointWithinPolygon(point, polygon) :
    return point.within(polygon)


def chechPointWithinPolygonList(point, polygonList) :
    for poly in polygonList:
        if point.within(poly) :
            return True

def getTransformer(fromCRS, toCRS):
    project = partial(
        pyproj.transform,
        pyproj.Proj(fromCRS),  # source coordinate system
        pyproj.Proj(toCRS))  # destination coordinate system
    return project

def getJerusalemBorder() :
    project = getTransformer('epsg:2039', 'epsg:4326')
    jerusalem_polygon = []
    polylist = list(
        csv.reader(open('/home/louis6/Documents/ness/MOT/mot_py/ressource/border2.csv', "rU"), delimiter='|'))
    for geom in polylist[0]:
        polygon = shapely.wkt.loads(geom)
        converted = transform(project, polygon)
        jerusalem_polygon.append(converted)
    return jerusalem_polygon
