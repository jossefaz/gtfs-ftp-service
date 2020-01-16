from shapely.geometry import Point
from utils.file import read_in_chunks
from utils.geometry import *
from utils.control import timing
from utils.path import *
import os
JERUSALEM = getJerusalemBorder()


@timing
def mainGeo() :
    workFile = os.path.join('/download/israel-public-transportation/stops.txt')
    with open(workFile) as f :
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


