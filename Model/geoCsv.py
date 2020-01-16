from shapely.geometry import Point
from utils.file import read_in_chunks
from utils.geometry import *
from utils.control import timing
from utils.path import *
import os



@timing
def checkPointsFromFile(dir, filename) :
    JERUSALEM = getJerusalemBorder()
    workFile = os.path.join(GetParentDir(os.path.dirname(__file__)), dir, filename)
    with open(workFile) as f :
        listofPoitn = []
        i = -1
        for chunk in read_in_chunks(f, 2048) :
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
                    chechPointWithinPolygonList(pointCheck, JERUSALEM) and listofPoitn.append([point[id_index], point[0], pointCheck])
                except :
                    continue
        print(len(listofPoitn))
        print(listofPoitn)

def checkLinesFromFile(dir, filename) :
    JERUSALEM = getJerusalemBorder()
    workFile = os.path.join(GetParentDir(os.path.dirname(__file__)), dir, filename)
    with open(workFile) as f :
        listofPoitn = []
        i = 0
        id_index = 0
        lat_index = 1
        lon_index = 2
        Current_route_points = []
        Current_route_id = -1
        Current_route_intersect = False
        for chunk in read_in_chunks(f, 2048) :
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
                                    Current_route_points.append(newPoint)
                                except :
                                    print("point {} of route {} cannot be converted to point".format(point[-1], Current_route_id))
                                pass




                        Current_route_id = point[id_index]
                        pointCheck = Point(float(point[lat_index]), float(point[lon_index]))
                        chechPointWithinPolygonList(pointCheck, JERUSALEM) and listofPoitn.append([Current_route_id, point[0], pointCheck])
                    except :
                        i += 1
                        continue
        print (i)
        print(len(listofPoitn))
        print(listofPoitn)