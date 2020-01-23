from collections import namedtuple

GEO= ['NAME','ITYPE','GEO_TYPE','AOI','FILTER_TYPE','RESULT_NAME']
ALPHA = ['NAME','ITYPE','PATH','JOIN_FIELD','FOOD_FIELDS', 'RESULT_NAME']
FUNC = ['NAME','ITYPE','RESULT_NAME']
TABLES = ['NAME','ITYPE','TABLES']
DB = ['NAME','ITYPE','RESULT_NAME', 'INSTANCE', 'ACTION', 'TABLE']

GEO_LINK = GEO.copy()+['LINKED_TO']
ALPHA_LINK = ALPHA.copy()+['LINKED_TO']
FUNC_LINK = ALPHA.copy()+['LINKED_TO']
TABLES_LINK = ALPHA.copy()+['LINKED_TO']
DB_LINK = DB.copy()+['LINKED_TO']

GEO_CB = GEO.copy()+['CB']
ALPHA_CB = ALPHA.copy()+['CB']
FUNC_CB = ALPHA.copy()+['CB']
TABLES_CB = ALPHA.copy()+['CB']
DB_CB = DB.copy()+['CB']

GEO_LINK_CB = GEO.copy()+['LINKED_TO','CB']
ALPHA_LINK_CB= ALPHA.copy()+['LINKED_TO','CB']
FUNC_LINK_CB = ALPHA.copy()+['LINKED_TO','CB']
TABLES_LINK_CB = ALPHA.copy()+['LINKED_TO','CB']
DB_LINK_CB = DB.copy()+['LINKED_TO','CB']

Igeo = namedtuple('Igeo', GEO)
Igeolink = namedtuple('Igeolink', GEO_LINK)
Igeocb = namedtuple('Igeocb', GEO_CB)
Igeolinkcb = namedtuple('Igeolinkcb', GEO_LINK_CB)

Ialpha = namedtuple('Ialpha', ALPHA)
Ialphalink = namedtuple('Ialphalink', ALPHA_LINK)
Ialphacb = namedtuple('Ialphacb', ALPHA_CB)
Ialphalinkcb = namedtuple('Ialphalinkcb', ALPHA_LINK_CB)

Ifunc = namedtuple('Ifunc', FUNC)
Ifunclink = namedtuple('Ifunclink', FUNC_LINK)
Ifunccb = namedtuple('Ifunccb', FUNC_CB)
Ifunclinkcb = namedtuple('Ifunclinkcb', FUNC_LINK_CB)

Itables = namedtuple('Itables', TABLES)
Itableslink = namedtuple('Itableslink', TABLES_LINK)
Itablescb = namedtuple('Itablescb', TABLES_CB)
Itableslinkcb = namedtuple('Itableslinkcb', TABLES_LINK_CB)

Idb = namedtuple('Idb', DB)
Idblink = namedtuple('Idblink', DB_LINK)
Idbcb = namedtuple('Idbcb', DB_CB)
Idblinkcb = namedtuple('Idblinkcb', DB_LINK_CB)


