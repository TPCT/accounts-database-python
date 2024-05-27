from configparser import ConfigParser
from os import path
from slowapi import Limiter
from slowapi.util import get_remote_address


config_parser = ConfigParser()
config_parser.read(path.join(path.dirname(__file__), '..', '.env'))

MONGO_DB = config_parser.get('DATABASE', 'MONGO_DB')
limiter = Limiter(key_func=get_remote_address)


