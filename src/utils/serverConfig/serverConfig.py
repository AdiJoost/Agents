from config.applicationConfig.applicationConfigFields import ApplicationConfigFields
from config.configFiles import ConfigFiles
from config.configManager import getConfig
from config.mongoDBConfig.mongoDbConfigFields import MongoDBConfigFields
from src.enums.deploymentMode import DeploymentMode
import os


class ServerConfig():

    @classmethod
    def getOllamaAddress(cls) -> str:
        deploymentMode = DeploymentMode(getConfig(ApplicationConfigFields.DEPLOYMENT_MODE.value))
        match deploymentMode:
            case DeploymentMode.LOCAL:
                return "http://localhost:11434"
            case DeploymentMode.SERVER:
                return os.environ["OLLAMA_HOST"]
            case DeploymentMode.DOCKER:
                return "http://ollama:11434"
            case _:
                return "http://localhost:11434"
            
    @classmethod
    def getMongoAddress(cls) -> str:
        deploymentMode = DeploymentMode(getConfig(ApplicationConfigFields.DEPLOYMENT_MODE.value))
        mongoDbHost = cls._getMongoDbHost(deploymentMode=deploymentMode)
        username = getConfig(MongoDBConfigFields.USERNAME.value, ConfigFiles.MONGO_DB_CONFIG)
        password = getConfig(MongoDBConfigFields.PASSWORD.value, ConfigFiles.MONGO_DB_CONFIG)
        port = getConfig(MongoDBConfigFields.PORT.value, ConfigFiles.MONGO_DB_CONFIG)
        match deploymentMode:
            case DeploymentMode.LOCAL:
                return f"mongodb://{username}:{password}@{mongoDbHost}:{port}/?authSource=admin"
            case DeploymentMode.SERVER:
                return f"mongodb://{mongoDbHost}:{port}/?authSource=admin"
            case DeploymentMode.DOCKER:
                return f"mongodb://{username}:{password}@{mongoDbHost}:{port}/?authSource=admin"
            case _:
                return f"mongodb://{username}:{password}@{mongoDbHost}:{port}/?authSource=admin"

    @classmethod     
    def _getMongoDbHost(cls, deploymentMode: DeploymentMode) -> str:
        match deploymentMode:
            case DeploymentMode.LOCAL:
                return "localhost"
            case DeploymentMode.SERVER:
                return os.environ["HOST_IP"]
            case DeploymentMode.DOCKER:
                return "mongodb"
            case _:
                return "localhost"