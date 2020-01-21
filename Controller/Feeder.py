# -*- coding: UTF-8 -*-
from Template.BaseClass import baseClass
import logging
import redis
import os
from utils.path import GetParentDir
from utils.control import timing
from utils.file import readHugeFile


class Feeder(baseClass) :

    __slots__ = ['logger', 'feed_file', 'joinF', 'fields', 'field_map_index', 'field_dict','id_result_hash', 'table_ref']

    def __init__(self, table_config, id_result_hash, table_ref):
        self.logger = logging.getLogger(__name__)
        self.feed_file = os.path.join(GetParentDir(os.path.dirname(__file__)), table_config.PATH, table_config.NAME)
        self.joinF = table_config.JOIN_FIELD
        self.fields = table_config.FOOD_FIELDS
        self.field_map_index = []
        self.field_dict = {}
        self.id_result_hash = id_result_hash
        self.table_ref = table_ref


    def exec(self, arg=None, cb=None):
        if cb is None:
            cb = []
        self.field_map_index, self.field_dict = self.fieldMapper()
        self.buildFoodStore()
        pass

    def fieldMapper(self):
        with open(self.feed_file, encoding='utf-8-sig') as f:
            ref_fields = f.readline().rstrip('\n').split(',')
        if self.fields is None :
            ref_fields = [i for i in range(0, len(ref_fields) - 1)]
            return ref_fields
        fields_filtered = []
        field_dict = {}
        for field in self.fields :
            if field not in  ref_fields:
                self.logger.warning("field {} of file {} from the ftp_url.yaml was not found in the downloaded file, check mispelling".format(field, self.file))
                continue

            fields_filtered.append(ref_fields.index(field))
            field_dict[ref_fields.index(field)] = field
        return fields_filtered, field_dict
    @timing
    def buildFoodStore(self):
        first_line = True
        index_field = 0

        conn = redis.StrictRedis(
            host='127.0.0.1',
            port=6543)
        with conn.pipeline() as pipe:

            pipeControl = 0
            readHugeFile(self.feed_file)
            with open(self.feed_file, encoding='utf-8-sig') as f:

                while True :
                    line = f.readline()
                    if line :
                        if first_line :
                            try:
                                index_field = line.rstrip('\n').split(',').index(self.joinF)
                                first_line = False
                                continue
                            except IndexError as e :
                                self.logger.error("the join attribute is not contained in the file : {}".format(self.file))
                                return None
                        if pipeControl %10 == 0 :
                            pipe.execute()
                        current_attr_lst = line.split(',')
                        current_id = current_attr_lst[index_field]
                        if self.id_result_hash.get(current_id, None) is not None:
                            # if current_id not in food_store :
                            #     food_store[current_id] = []
                            attr_dict = {}
                            for i in self.field_map_index :
                                attr_dict[self.field_dict[i]] = current_attr_lst[i]
                            pipe.hmset(current_id, attr_dict)
                            pipeControl +=1
                    else :
                        break

        pipe.execute()
        conn.save()


    def feedIt(self, hungry_data_struct):
        pass


if __name__ == '__main__' :
    conn = redis.StrictRedis(
        host='127.0.0.1',
        port=6543)
    conn.set()