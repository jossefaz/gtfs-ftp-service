from collections import namedtuple

ftp_geo_file_props = ['NAME', 'GEO_TYPE', 'AOI', 'FILTER_TYPE', 'FILE_TYPE']
ftp_feeder_file_props = ['NAME', 'JOIN_FIELD', 'FOOD_FIELDS', 'PATH']


ftp_geo_file = namedtuple('ftp_geo_file', ftp_geo_file_props)
ftp_feeder_file = namedtuple('ftp_geo_file', ftp_feeder_file_props)


