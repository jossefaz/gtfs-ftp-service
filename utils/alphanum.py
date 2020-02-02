from utils.control import timing
import mysql.connector
def fieldMapper(file,fields, logger):
    with open(file, encoding='utf-8-sig') as f:
        ref_fields = f.readline().rstrip('\n').split(',')
    if fields is None :
        ref_fields = [i for i in range(0, len(ref_fields) - 1)]
        return ref_fields
    fields_filtered = []
    field_dict = {}
    for field in fields :
        if field not in  ref_fields:
            logger.warning("field {} of file {} from the pipeline.yaml was not found in the downloaded file, check mispelling".format(field, file))
            continue
        fields_filtered.append(ref_fields.index(field))
        field_dict[ref_fields.index(field)] = field
    return fields_filtered, field_dict

def defineIndexes(workFile) :
    with open(workFile, encoding='utf-8-sig') as f:
        line = f.readline()
        for p in filter(None, line.split('\n')):
                columns = p.split(',')
                id_indexes = {index_name : index for index, index_name in enumerate(columns) if 'id' in index_name}
        return id_indexes


@timing
def getAlphanumById(file, id_hash, id_field, logger, field_map_index, field_dict, fields=None) :
    id_indexes = defineIndexes(workFile=file)
    first_line = True
    alphanum = []
    hash_id = {}
    with open(file, encoding='utf-8-sig') as f:
            while True :
                line = f.readline()
                if line :
                    if first_line :
                        try:
                            index_field = id_indexes.get(id_field)
                            first_line = False
                            continue
                        except IndexError as e :
                            logger.error("the join attribute is not contained in the file : {}".format(file))
                            return None
                    current_attr_lst = line.strip('\n').split(',')
                    current_id = current_attr_lst[index_field]
                    if id_hash.get(id_field).get(current_id, None):
                        for id, index in id_indexes.items() :
                            if id not in hash_id :
                                hash_id[id] = {}
                            hash_id[id][current_attr_lst[index]] = current_attr_lst[index]
                        attr_dict = {}
                        for i in field_map_index :
                            if field_dict[i] in fields :
                                attr_dict[field_dict[i]] = current_attr_lst[i]
                        alphanum.append(attr_dict)

                else :
                    break
    return { "result" : alphanum, "ids" : hash_id}


if __name__ == '__main__' :
    pass
