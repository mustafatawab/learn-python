from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()


DATABASE_URL = Config('DATABASE_URL' , cast=Secret)