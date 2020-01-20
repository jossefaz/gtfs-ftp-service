# -*- coding: UTF-8 -*-
from Template.BaseClass import baseClass
import logging
from registry.controller import registry

class Feeder(baseClass) :

    __slots__ = ['logger', 'registry', 'file', 'joinF', 'fields', 'field_map', 'id_index_list']

    def __init__(self, feed_file, id_index_list, join_attribute, fields_to_include=None):
        self.logger = logging.getLogger(__name__)
        self.registry = registry[self.__class__.__name__]
        self.feed_file = feed_file
        self.joinF = join_attribute
        self.fields = fields_to_include
        self.field_map = []
        self.id_index_list = id_index_list


    def exec(self, hungry_data_struct=None, cb=None):
        if hungry_data_struct is None :
            self.logger.error("You must provide a data structure to feed")
            return None
        self.field_map = self.fieldMapper()



        pass

    def fieldMapper(self):
        with open(self.feed_file, encoding='utf-8-sig') as f:
            ref_fields = f.readline().split(',')
        if self.fields is None :
            ref_fields = [i for i in range(0, len(ref_fields) - 1)]
            return ref_fields
        fields_filtered = []
        for field in self.fields :
            if field not in  ref_fields:
                self.logger.warning("field {} of file {} from the ftp_url.yaml was not found in the downloaded file, check mispelling".format(field, self.file))
                continue

            fields_filtered.append(ref_fields.index(field))
        return fields_filtered

    def buildFoodStore(self):
        first_line = True
        index_field = 0
        with open(self.feed_file, encoding='utf-8-sig') as f:
            for line in f :
                if first_line :
                    try:
                        index_field = line.split(',').index(self.joinF)
                        continue
                    except IndexError as e :
                        self.logger.error("the join attribute is not contained in the file : {}".format(self.file))
                        return None
                if line.split(',')[index_field] in self.id_index_list :
                    print('found')



    def feedIt(self, hungry_data_struct):
        pass


if __name__ == '__main__' :
    test = Feeder('/home/louis6/Documents/ness/MOT/mot_py/download/trips.txt', 'shape_id', ['test', 'direction_id' ])
    test.exec()