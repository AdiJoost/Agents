from config.applicationConfig.applicationConfigFields import ApplicationConfigFields
from config.configManager import getConfig
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
        match deploymentMode:
            case DeploymentMode.LOCAL:
                return "localhost"
            case DeploymentMode.SERVER:
                return os.environ["HOST_IP"]
            case DeploymentMode.DOCKER:
                return "mongodb"
            case _:
                return "localhost"