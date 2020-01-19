import hiyapyco
import sys
import os
import logging
from Template.BaseClass import baseClass

configFiles = {
    "DEV" : "config_dev.yaml",
    "PROD" : "config.yaml",
    "NOT_FOUND" : "Only DEV or PROD argument is allowed"

}



class Config(baseClass):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._config = self.load_config()

    def exec(self):
        pass
    def load_config(self) :
        if configFiles.get(sys.argv[1]) is None :
            self.logger.error(configFiles.get("NOT_FOUND"))
            sys.exit(1)
        config_file = os.path.join(os.path.dirname(__file__), configFiles.get(sys.argv[1]))
        ftp_urls = os.path.join(os.path.dirname(__file__),'ftp_url.yaml')
        conf = hiyapyco.load(config_file, ftp_urls, method=hiyapyco.METHOD_MERGE, interpolate=True,
                             failonmissingfiles=True)
        return conf

    def get_property(self, property_name):
        if property_name not in self._config.keys(): 
            return None
        return self._config[property_name]

