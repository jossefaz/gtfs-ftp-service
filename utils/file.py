#-*- coding: UTF-8 -*-

import csv, sqlite3, sys
import multiprocessing as mp, os
from multiprocessing import cpu_count

first_line = True
index_field = 0
pipeControl = 0
# conn = redis.StrictRedis(
#     host='127.0.0.1',
#     port=6543)
def read_in_chunks(file_object, chunk_size=1024):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data






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
def readHugeFile(fname, joinF, id_result_hash, field_map_index, field_dict) :
    #init objects
    pool = mp.Pool(cpu_count())
    jobs = []

    #create jobs
    for chunkStart,chunkSize in chunkify(fname):
        jobs.append( pool.apply_async(process_wrapper,(chunkStart,chunkSize, fname, joinF, id_result_hash, field_map_index, field_dict)) )

    #wait for all jobs to finish
    for job in jobs:
        job.get()

    #clean up
    pool.close()

if __name__ == "__main__":
    pass
    # data_file_name = '/home/louis6/Documents/ness/MOT/mot_py/download/stop_times.txt'
    #
    # # importing pandas package
    # import pandas as pd
    # from sqlalchemy import create_engine
    #
    # engine = create_engine('sqlite://', echo=False)
    # # making data frame from csv file
    # data = pd.read_csv(data_file_name)
    # df = pd.DataFrame(data)
    # df.to_sql('stops_time', con=engine)
    # cur = engine.execute("SELECT * FROM stops_time WHERE stop_id = 3803").fetchall()
    # for i in cur.fetchall() :
    #     print(i)




