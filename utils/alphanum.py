
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