import csv
from functools import partial
from shapely.ops import transform
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


@timing
def checkPointsFromFile(workFile, AOI, filterType) :
    with open(workFile, encoding='utf-8') as f :
        all_points = {}
        i = -1
        for chunk in f:
            for p in filter(None, chunk.split('\n')) :
                if i == -1 :
                    columns = p.split(',')
                    id_index = [i for i, s in enumerate(columns) if 'id' in s][0]
                    lat_index = [i for i, s in enumerate(columns) if 'lat' in s][0]
                    lon_index = [i for i, s in enumerate(columns) if 'lon' in s][0]
                    i = 0
                try:
                    point = p.split(',')
                    pointCheck = Point(float(point[lat_index]), float(point[lon_index]))
                    if checkPointPolygonList(pointCheck, AOI, filterType) :
                        all_points[point[id_index]] = [p, pointCheck.wkt]
                #Commentaire
                except :
                    continue
        return all_points

@timing
def checkLinesFromFile(workFile, AOI, filterType):
    '''

    :param workFile:  Must be ordered by route_id
    :param geoMask:
    :param filterType:
    :return:
    '''
    with open(workFile, encoding='utf-8') as f :
        All_routes = {}
        i = 0
        id_index = 0
        lat_index = 1
        lon_index = 2
        Current_route_points = []
        Current_route_id = -1
        Current_route_intersect = False
        for chunk in f:
            for p in filter(None, chunk.split('\n')) :
                if Current_route_id == -1 :
                    columns = p.split(',')
                    id_index = [i for i, s in enumerate(columns) if 'id' in s][0]
                    lat_index = [i for i, s in enumerate(columns) if 'lat' in s][0]
                    lon_index = [i for i, s in enumerate(columns) if 'lon' in s][0]
                    Current_route_id  = 0
                else :
                    try:
                        point = p.split(',')
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
                            Current_route_points = []

                        Current_route_id = point[id_index]
                        Current_route_intersect = False
                        #try to conver to Point :
                        try:
                            pointCheck = Point(float(point[lat_index]), float(point[lon_index]))
                            if checkPointPolygonList(pointCheck, AOI, filterType) :
                                Current_route_points.append(pointCheck)
                                Current_route_intersect = True
                        except Exception as e:
                            print(str(e))
                            # print("point {} of route {} cannot be converted to point".format(point[-1], Current_route_id))
                            continue

                    except :
                        i += 1
                        continue
        return All_routes
