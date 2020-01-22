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
            logger.warning("field {} of file {} from the ftp_url.yaml was not found in the downloaded file, check mispelling".format(field, file))
            continue
        fields_filtered.append(ref_fields.index(field))
        field_dict[ref_fields.index(field)] = field
    return fields_filtered, field_dict
@timing
def getAlphanumById(file, id_hash, id_field, logger, field_map_index, field_dict) :
    first_line = True
    alphanum = {}
    with open(file, encoding='utf-8-sig') as f:
            while True :
                line = f.readline()
                if line :
                    if first_line :
                        try:
                            index_field = line.rstrip('\n').split(',').index(id_field)
                            first_line = False
                            continue
                        except IndexError as e :
                            logger.error("the join attribute is not contained in the file : {}".format(file))
                            return None
                    current_attr_lst = line.split(',')
                    current_id = current_attr_lst[index_field]
                    if id_hash.get(current_id, None):
                        if current_id not in alphanum :
                            alphanum[current_id] = []
                        attr_dict = {}
                        for i in field_map_index :
                            attr_dict[field_dict[i]] = current_attr_lst[i]
                        alphanum[current_id].append(attr_dict)

                else :
                    break
    return alphanum

def insertToAlphanumDB(dictValue, table_name, connection_string) :
    mydb = mysql.connector.connect(
        host="localhost",
        user="louis6",
        passwd="dev123",
    database = "sde"
    )
    mycursor = mydb.cursor()
    ins_qry = "INSERT INTO {tablename} ({columns}) VALUES {values};".format(
        tablename='stop_times',
        columns=', '.join(dictValue.keys()),
        values=tuple(dictValue.values())
    )
    mycursor.execute(ins_qry)
    mydb.commit()
    return True

if __name__ == '__main__' :
    pass
