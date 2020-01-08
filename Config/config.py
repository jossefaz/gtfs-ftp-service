import yaml

class Config(object):
    def __init__(self):
        self._config = self.load_config()
        
    def load_config() :
        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

    def get_property(self, property_name):
        if property_name not in self._config.keys(): 
            return None
        return self._config[property_name]
    