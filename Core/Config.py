from configparser import ConfigParser
from os import path


config_parser = ConfigParser()
config_parser.read(path.join(path.dirname(__file__), '..', '.env'))

MONGO_DB = config_parser.get('DATABASE', 'MONGO_DB')
