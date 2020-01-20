# -*- coding: UTF-8 -*-
from Template.BaseClass import baseClass
import logging


class Feeder(baseClass) :

    __slots__ = ['logger', 'feed_file', 'joinF', 'fields', 'field_map_index', 'field_dict','id_index_list']

    def __init__(self, feed_file, id_index_list, join_attribute, fields_to_include=None):
        self.logger = logging.getLogger(__name__)

        self.feed_file = feed_file
        self.joinF = join_attribute
        self.fields = fields_to_include
        self.field_map_index = []
        self.field_dict = {}
        self.id_index_list = id_index_list


    def exec(self, hungry_data_struct=None, cb=None):
        if hungry_data_struct is None :
            self.logger.error("You must provide a data structure to feed")
            return None
        self.field_map_index, self.field_dict = self.fieldMapper()
        food_store = self.buildFoodStore()
        print(food_store)



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

    def buildFoodStore(self):
        first_line = True
        index_field = 0
        food_store = {}
        with open(self.feed_file, encoding='utf-8-sig') as f:
            for line in f :
                if first_line :
                    try:
                        index_field = line.rstrip('\n').split(',').index(self.joinF)
                        first_line = False
                        continue
                    except IndexError as e :
                        self.logger.error("the join attribute is not contained in the file : {}".format(self.file))
                        return None
                current_attr_lst = line.split(',')
                current_id = current_attr_lst[index_field]
                if current_id in self.id_index_list :
                    if current_id not in food_store :
                        food_store[current_id] = []
                    attr_dict = {}
                    for i in self.field_map_index :
                        attr_dict[self.field_dict[i]] = current_attr_lst[i]
                    food_store[current_id].append(attr_dict)




    def feedIt(self, hungry_data_struct):
        pass


if __name__ == '__main__' :
    test = Feeder('/home/louis6/Documents/ness/MOT/mot_py/download/trips.txt', 'shape_id', ['test', 'direction_id' ])
    test.exec()