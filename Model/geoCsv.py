from shapely.geometry import Point
from utils.file import read_in_chunks
from utils.geometry import *
from utils.control import timing
from utils.path import *
import os



@timing
def mainGeo() :
    JERUSALEM = getJerusalemBorder()
    workFile = os.path.join(GetParentDir(os.path.dirname(__file__)), 'download/israel-public-transportation/stops.txt')
    with open(workFile) as f :
        listofPoitn = []
        i = 0
        j = 0
        for chunk in read_in_chunks(f, 2048) :
            Current_route_points = []
            Current_route_id = -1
            Current_route_intersect = False
            for p in filter(None, chunk.split('\n')) :
                try:
                    point = p.split(',')
                    pointCheck = Point(float(point[4]), float(point[5]))
                    chechPointWithinPolygonList(pointCheck, JERUSALEM) and listofPoitn.append([point[-1], point[0], pointCheck])
                except :
                    i += 1
                    continue
        print (i)
        print(len(listofPoitn))
        print(listofPoitn)
