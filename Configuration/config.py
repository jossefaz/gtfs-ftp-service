import yaml
import sys
import os
import logging
from Templates.BaseClass import baseClass

configFiles = {
    "DEV" : "config_dev.yaml",
    "PROD" : "config.yaml",
    "NOT_FOUND" : "Only DEV or PROD argument is allowed"
}



class Config(baseClass):

    def __init__(self):
        self._config = self.load_config()

    def setClassLogger(self):
        self.logger = logging.getLogger(__name__)
        
    def load_config(self) :

        config_file = configFiles.get(sys.argv[1])
        if config_file is None :
            raise ValueError(configFiles.get("NOT_FOUND"))
        with open(os.path.join(os.path.dirname(__file__),config_file), 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile.read())
            return cfg

    def get_property(self, property_name):
        if property_name not in self._config.keys(): 
            return None
        return self._config[property_name]
    