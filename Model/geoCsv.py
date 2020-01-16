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

checkPointsFromFile('download/israel-public-transportation', 'stops.txt')