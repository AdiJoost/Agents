from enum import Enum

class MongoDBConfigFields(Enum):
    HOST = "HOST"
    PORT = "PORT"
    USERNAME = "USERNAME"
    PASSWORD = "PASSWORD"
    DATABASE_NAME = "DATABASE_NAME"