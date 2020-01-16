from shapely.geometry import Point
from utils.file import read_in_chunks
from utils.geometry import *
from utils.control import timing
JERUSALEM = getJerusalemBorder()


@timing
def mainGeo() :
    with open('/home/louis6/Documents/ness/MOT/mot_py/download/israel-public-transportation/stops.txt') as f :
        listofPoitn = []
        i = 0
        j = 0
        for chunk in read_in_chunks(f, 2048) :
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


