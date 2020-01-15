from shapely.geometry import Point
from utils.file import read_in_chunks
from utils.geometry import *
from utils.control import timing
JERUSALEM = getJerusalemBorder()

@timing
def mainGeo() :
    with open('/home/louis6/Documents/ness/MOT/mot_py/download/israel-public-transportation/shapes.txt') as f :
        listofPoitn = []
        for chunk in read_in_chunks(f, 2048) :
            for p in filter(None, chunk.split('\n')) :
                try:
                    point = p.split(',')
                    pointCheck = Point(float(point[1]), float(point[2]))
                    chechPointWithinPolygonList(pointCheck, JERUSALEM) and listofPoitn.append([point[-1], point[0], pointCheck])
                except :
                    continue
        print(listofPoitn)


mainGeo()