import csv
from functools import partial
from shapely.ops import transform
from shapely.geometry import Point, LineString
from utils.projections import *
from utils.control import timing
from utils.path import *
from collections import namedtuple
import os


import shapely.wkt
def chechPointWithinPolygon(point, polygon) :
    return point.within(polygon)


def checkPointPolygonList(point, polygonList, filtertype) :
    for poly in polygonList:
        if point.within(poly) :
            return True
    return False

def getTransformer(fromCRS, toCRS):
    project = partial(pyproj.transform,fromCRS, toCRS)
    return project

def transformWKT(feature, fromCRS, toCRS) :
    project = getTransformer(projections[fromCRS], projections[toCRS])
    converted = transform(project, feature)
    return converted.wkt



def getJerusalemBorder() :
    project = getTransformer(projections['wgs84'], projections['israel'])
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
    with open(workFile, encoding='utf-8-sig') as f:
        line = f.readline()
        for p in filter(None, line.split('\n')):
                columns = p.split(',')
                id_index = [i for i, s in enumerate(columns) if 'id' in s][0]
                lat_index = [i for i, s in enumerate(columns) if 'lat' in s][0]
                lon_index = [i for i, s in enumerate(columns) if 'lon' in s][0]
        return id_index, lat_index, lon_index



@timing
def checkPointsFromFile(workFile, AOI, filterType) :
    id_index, lat_index, lon_index = defineIndexes(workFile)
    all_points = {}
    hash_id = {}
    firstLine = -1
    attrTuple = None
    with open(workFile, encoding='utf-8-sig') as f :
        for line in f:
                if firstLine == -1 :
                    attr_list = [i for j, i in enumerate(line.strip('\n').split(',')) if j not in [lat_index, lon_index]]
                    attrTuple = namedtuple('attributes', attr_list)
                    firstLine = 0
                    continue
                try:
                    point = line.strip('\n').split(',')
                    pointCheck = Point(float(point[lat_index]), float(point[lon_index]))
                    if checkPointPolygonList(pointCheck, AOI, filterType) :
                        attr_list = [i for j, i in enumerate(point) if j not in [lat_index, lon_index]]
                        all_points[point[id_index]] = {'attr' : attrTuple(*attr_list), 'geom' : pointCheck}
                        hash_id[point[id_index]] = point[id_index]
                #Commentaire
                except Exception as e:
                    print(str(e))
                    continue
        return { "result" : all_points, "ids" : hash_id}

@timing
def checkLinesFromFile(workFile, AOI, filterType):
    '''

    :param workFile:  Must be ordered by route_id
    :param AOI:
    :param filterType:
    :return:
    '''
    id_index, lat_index, lon_index = defineIndexes(workFile)
    All_routes = {}
    hash_id = {}
    i = 0
    attrTuple = None
    Current_route_points = []
    Current_route_id = -1
    Current_route_intersect = False
    with open(workFile, encoding='utf-8-sig') as f :

        for line in f:
            if Current_route_id == -1 :
                attrTuple = namedtuple('attributes', line.strip('\n').split(','))
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
                    All_routes[Current_route_id] = {'attr' : attrTuple(*point), 'geom' : LineString(Current_route_points)}
                    hash_id[Current_route_id] = Current_route_id
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
        return { "result" : All_routes, "ids" : hash_id}
