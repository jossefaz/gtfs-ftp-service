import csv
from functools import partial
from shapely.ops import transform
from shapely.ops import cascaded_union
from shapely.geometry import Point
from utils.projections import *
from utils.control import timing
from utils.path import *
import os

import shapely.wkt
def chechPointWithinPolygon(point, polygon) :
    return point.within(polygon)


def checkPointPolygonList(point, polygonList, filtertype) :
    check = False
    for poly in polygonList:
        if point.within(poly) :
            check = True if filtertype == 'within' else False
        else :
            check = False if filtertype == 'within' else True
    return check

def checkPointMultipolygon(point, multipolygon, filtertype) :
    if point.within(multipolygon) :
        return True
    return False


def checkPointInExtent(x, y, multipolygon, filtertype):
    extent = multipolygon.bounds
    check = ((x > extent[0] and x < extent[2]) and (y > extent[1] and y < extent[3]) ) and filtertype == 'within'
    if check:
        return checkPointMultipolygon(Point(x,y), multipolygon, filtertype)
    return False

def checkPointInExtentList(x, y, polygons, filtertype):
    for polygon in polygons :
        extent = polygon.bounds
        check = ((x > extent[0] and x < extent[2]) and (y > extent[1] and y < extent[3]) ) and filtertype == 'within'
        if check:
            return checkPointPolygonList(Point(x,y), polygons, filtertype)
    return False

def getTransformer(fromCRS, toCRS):
    project = partial(pyproj.transform,fromCRS, toCRS)
    return project

def getJerusalemBorder() :
    project = getTransformer(israel_tm_grid, wgs84)
    jerusalem_polygon = []
    workFile = os.path.join(GetParentDir(os.path.dirname(__file__)), 'ressource/border2.csv')
    polylist = list(csv.reader(open(workFile, 'r'), delimiter='|'))
    for geom in polylist[0]:
        polygon = shapely.wkt.loads(geom)
        converted = transform(project, polygon)
        jerusalem_polygon.append(converted)
    return jerusalem_polygon

if __name__ == '__main__' :
    getJerusalemBorder()

def defineIndexes(workFile) :
    with open(workFile, encoding='utf-8') as f:
        line = f.readline()
        for p in filter(None, line.split('\n')):
                columns = p.split(',')
                id_index = [i for i, s in enumerate(columns) if 'id' in s][0]
                lat_index = [i for i, s in enumerate(columns) if 'lat' in s][0]
                lon_index = [i for i, s in enumerate(columns) if 'lon' in s][0]
        return id_index, lat_index, lon_index


@timing
def checkPointsFromFile(workFile, AOI, filterType) :
    with open(workFile, encoding='utf-8') as f :
        all_points = {}
        hash_id = {}
        firstLine = -1
        id_index, lat_index, lon_index = defineIndexes(workFile)
        for line in f:
                if firstLine == -1 :
                    firstLine = 0
                    continue
                try:
                    point = line.strip('\n').split(',')
                    pointCheck = checkPointInExtentList(float(point[lat_index]), float(point[lon_index]), AOI, filterType)
                    if pointCheck :
                        all_points[point[id_index]] = [line.strip('\n'), Point(float(point[lat_index]), float(point[lon_index]))]
                        hash_id[point[id_index]] = point[id_index]
                #Commentaire
                except :
                    continue
        return all_points, hash_id


@timing
def checkLinesFromFile(workFile, AOI, filterType):
    '''

    :param workFile:  Must be ordered by route_id
    :param AOI:
    :param filterType:
    :return:
    '''

    with open(workFile, encoding='utf-8') as f :
        All_routes = {}
        hash_id = {}
        i = 0
        id_index,lat_index,lon_index = defineIndexes(workFile)
        Current_route_points = []
        Current_route_id = -1
        Current_route_intersect = False
        for line in f:
            if Current_route_id == -1 :
                Current_route_id  = 0
                continue
            try:
                point = line.strip('\n').split(',')
                #Check if aleready loop on this id
                if point[id_index] == Current_route_id :
                    # Check if poitn intersect
                    if Current_route_intersect :
                        # try to convert to Point :
                        try :
                            newPoint = Point(float(point[lat_index]), float(point[lon_index]))
                            #Add new point to points list
                            Current_route_points.append(newPoint)
                            continue
                        except Exception as e:
                            print(str(e))
                            # print("point {} of route {} cannot be converted to point".format(point[-1], Current_route_id))
                            continue
                # NEW ROUTE
                #set the new Current route id
                if len(Current_route_points) > 0 :
                    All_routes[Current_route_id] = Current_route_points
                    hash_id[Current_route_id] = Current_route_id
                    Current_route_points = []

                Current_route_id = point[id_index]
                Current_route_intersect = False
                #try to conver to Point :
                try:
                    pointCheck = checkPointInExtentList(float(point[lat_index]), float(point[lon_index]), AOI, filterType)
                    if pointCheck :
                        Current_route_points.append(Point(float(point[lat_index]), float(point[lon_index])))
                        Current_route_intersect = True
                except Exception as e:
                    print(str(e))
                    # print("point {} of route {} cannot be converted to point".format(point[-1], Current_route_id))
                    continue

            except :
                i += 1
                continue
        return All_routes, hash_id
