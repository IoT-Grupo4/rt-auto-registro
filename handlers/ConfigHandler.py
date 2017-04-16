import sys
import os
import yaml

class ConfigHandler:

    # Le o arquivo de configuração              
    config_file_stream = open(os.path.join(sys.path[0], "config.yaml"), "r")
    config = yaml.load(config_file_stream)