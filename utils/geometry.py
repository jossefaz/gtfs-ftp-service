import csv
from functools import partial
from shapely.ops import transform
from shapely.geometry import Point
from utils.projections import *
from utils.control import timing
from utils.path import *
import multiprocessing as mp, os
from multiprocessing import cpu_count
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
        hash_id = {}
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
                        hash_id[point[id_index]] = point[id_index]
                #Commentaire
                except :
                    continue
        return all_points, hash_id

def defineIndexes(workFile) :
    with open(workFile, encoding='utf-8') as f:
        line = f.readline()
        for p in filter(None, line.split('\n')):
                columns = p.split(',')
                id_index = [i for i, s in enumerate(columns) if 'id' in s][0]
                lat_index = [i for i, s in enumerate(columns) if 'lat' in s][0]
                lon_index = [i for i, s in enumerate(columns) if 'lon' in s][0]
        return id_index, lat_index, lon_index
    


def checkLines(chunkStart, chunkSize, workFile, AOI, filterType, id_index, lat_index, lon_index):

    with open(workFile, encoding='utf-8') as f :
        Current_route_points = []
        Current_route_intersect = False
        Current_route_id = 0
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        for chunk in lines:
                    try:
                        point = chunk.strip('\n').split(',')
                        #Check if aleready loop on this id
                        if point[id_index] == Current_route_id :

                            # Check if poitn intersect
                            if Current_route_intersect :
                                # try to convert to Point :
                                try :
                                    newPoint = Point(float(point[lat_index]), float(point[lon_index ]))
                                    #Add new point to points list
                                    Current_route_points.append(newPoint)
                                    continue
                                except Exception as e:
                                    # print(str(e))
                                    # print("point {} of route {} cannot be converted to point".format(point[-1], Current_route_id))
                                    continue
                        # NEW ROUTE
                        #set the new Current route id
                        if len(Current_route_points) > 0 :
                            #TODO Insert in db
                            # if Current_route_id in All_routes :
                            #     All_routes[Current_route_id].append(Current_route_points)
                            # else :
                            #     All_routes[Current_route_id] = Current_route_points
                            # hash_id[Current_route_id] = Current_route_id
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
                            # print(str(e))
                            # print("point {} of route {} cannot be converted to point".format(point[-1], Current_route_id))
                            continue

                    except :
                        continue

def chunkify(fname,size=1024*1024):
    fileEnd = os.path.getsize(fname)
    with open(fname,'rb') as f:
        chunkEnd = f.tell()
        while True:
            chunkStart = chunkEnd
            f.seek(size,1)
            f.readline()
            chunkEnd = f.tell()
            yield chunkStart, chunkEnd - chunkStart
            if chunkEnd > fileEnd:
                break
@timing
def checkLinesFromFile(workFile, AOI, filterType) :
    #init objects
    pool = mp.Pool(1)
    jobs = []
    All_routes = {}
    hash_id = {}
    id_index, lat_index, lon_index = defineIndexes(workFile)
    #create jobs
    for chunkStart,chunkSize in chunkify(workFile):
        jobs.append( pool.apply_async(checkLines,(chunkStart,chunkSize, workFile, AOI, filterType, id_index, lat_index, lon_index)) )

    #wait for all jobs to finish
    for job in jobs:
        job.get()

    #clean up
    pool.close()

