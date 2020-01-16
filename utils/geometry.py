import csv
from functools import partial
from shapely.ops import transform
from utils.projections import *
from utils.path import *
import os

import shapely.wkt
def chechPointWithinPolygon(point, polygon) :
    return point.within(polygon)


def chechPointWithinPolygonList(point, polygonList) :
    for poly in polygonList:
        if point.within(poly) :
            return True

def getTransformer(fromCRS, toCRS):
    project = partial(pyproj.transform,fromCRS, toCRS)
    return project

def getJerusalemBorder() :
    project = getTransformer(israel_tm_grid, wgs84)
    jerusalem_polygon = []
    workFile = os.path.join(GetParentDir(os.path.dirname(__file__)), 'ressource/border2.csv')
    polylist = list(
        csv.reader(open(workFile, "rU"), delimiter='|'))
    for geom in polylist[0]:
        polygon = shapely.wkt.loads(geom)
        converted = transform(project, polygon)
        jerusalem_polygon.append(converted)
    return jerusalem_polygon

if __name__ == '__main__' :
    getJerusalemBorder()