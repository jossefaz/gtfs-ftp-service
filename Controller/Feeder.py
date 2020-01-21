# -*- coding: UTF-8 -*-
from Template.BaseClass import baseClass
import logging
import redis
from utils.control import timing
from utils.file import readHugeFile


class Feeder(baseClass) :

    __slots__ = ['logger', 'feed_file', 'joinF', 'fields', 'field_map_index', 'field_dict','id_result_hash', 'pipe', 'first_line', 'index_field', 'pipeControl']

    def __init__(self, feed_file, id_result_hash, join_attribute, fields_to_include=None):
        self.logger = logging.getLogger(__name__)

        self.feed_file = feed_file
        self.joinF = join_attribute
        self.fields = fields_to_include
        self.field_map_index = []
        self.field_dict = {}
        self.id_result_hash = id_result_hash
        self.pipe = None
        self.first_line = True
        self.index_field = 0
        self.pipeControl = 0


    def exec(self, hungry_data_struct=None, cb=None):
        if hungry_data_struct is None :
            self.logger.error("You must provide a data structure to feed")
            return None
        # self.field_map_index, self.field_dict = self.fieldMapper()
        # food_store = self.buildFoodStore()
        # print(food_store)
        return [1]



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
        readHugeFile(self.feed_file, self.joinF, self.id_result_hash, self.field_map_index, self.field_dict)


    def feedIt(self, hungry_data_struct):
        pass


if __name__ == '__main__' :
    conn = redis.StrictRedis(
        host='127.0.0.1',
        port=6543)
    conn.set()