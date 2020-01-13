import logging
import logging.config
import yaml
import os
import sys
configFiles = {
    "DEV" : "log_config.yaml",
    "PROD" : "log_config.yaml",
    "NOT_FOUND" : "Only DEV or PROD argument is allowed"
}
def setupLogging():
    config_file = configFiles.get(sys.argv[1])
    if config_file is None:
        config_file = "log_config.yaml"
    with open(os.path.join(os.path.dirname(__file__),config_file), 'rt') as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)
