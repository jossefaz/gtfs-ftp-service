import yaml



class Config(object):
    def __init__(self):
        self._config = conf # set it to conf
        
    def load_config() :
        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

    def get_property(self, property_name):
        if property_name not in self._config.keys(): # we don't want KeyError
            return None  # just return None if not found
        return self._config[property_name]
    