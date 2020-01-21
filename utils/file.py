#-*- coding: UTF-8 -*-

import csv, sqlite3, sys
import multiprocessing as mp, os
from multiprocessing import cpu_count
import redis
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
def process_wrapper(chunkStart, chunkSize, fname, joinF, id_result_hash, field_map_index, field_dict):

    with open(fname) as f:
        global index_field
        global pipeControl
        global first_line
        global conn
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        for line in lines:
            with conn.pipeline() as pipe:
                if first_line:
                    try:
                        index_field = line.rstrip('\n').split(',').index(joinF)
                        first_line = False
                    except IndexError as e:
                        print(str(e))
                        return None
                else:
                    if pipeControl % 10 == 0:
                        pipe.execute()
                    current_attr_lst = line.split(',')
                    current_id = current_attr_lst[index_field]
                    if id_result_hash.get(current_id, None) is not None:
                        # if current_id not in food_store :
                        #     food_store[current_id] = []
                        attr_dict = {}
                        for i in field_map_index:
                            attr_dict[field_dict[i]] = current_attr_lst[i]
                        pipe.hmset(current_id, attr_dict)
                        pipeControl += 1




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

    data_file_name = '/home/louis6/Documents/ness/MOT/mot_py/download/stop_times.txt'

    # importing pandas package
    import pandas as pd
    from sqlalchemy import create_engine

    engine = create_engine('sqlite://', echo=False)
    # making data frame from csv file
    data = pd.read_csv(data_file_name)
    df = pd.DataFrame(data)
    df.to_sql('stops_time', con=engine)
    cur = engine.execute("SELECT * FROM stops_time WHERE stop_id = 3803").fetchall()
    for i in cur.fetchall() :
        print(i)




