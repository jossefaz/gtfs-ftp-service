import yaml
import sys
import os
configFiles = {
    "DEV" : "config_dev.yaml",
    "PROD" : "config.yaml"
}

class Config(object):
    def __init__(self):
        self._config = self.load_config()
        
    def load_config(self) :
        config_file = configFiles.get(sys.argv[1])
        with open(os.path.join(os.path.dirname(__file__),config_file), 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
            return cfg

    def get_property(self, property_name):
        if property_name not in self._config.keys(): 
            return None
        return self._config[property_name]
    