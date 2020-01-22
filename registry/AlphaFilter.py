from utils.alphanum import getAlphanumById
from utils.dummy import printFoo
REGISTRY = {
    "filter": {
        "by_id": getAlphanumById,
        "by_sql" : "by_sql"
    },
    "callbacks": {
        "printFoo": printFoo
    }
}