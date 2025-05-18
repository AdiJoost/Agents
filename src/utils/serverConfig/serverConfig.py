from config.applicationConfig.applicationConfigFields import ApplicationConfigFields
from config.configManager import getConfig
from src.enums.deploymentMode import DeploymentMode


class ServerConfig():

    @classmethod
    def getOllamaAddress(cls) -> str:
        deploymentMode = DeploymentMode(getConfig(ApplicationConfigFields.DEPLOYMENT_MODE.value))
        match deploymentMode:
            case DeploymentMode.LOCAL | DeploymentMode.SERVER:
                return "http://localhost:11434"
            case DeploymentMode.DOCKER:
                return "http://ollama:11434"
            case _:
                return "http://localhost:11434"
            
    @classmethod
    def getMongoAddress(cls) -> str:
        deploymentMode = DeploymentMode(getConfig(ApplicationConfigFields.DEPLOYMENT_MODE.value))
        match deploymentMode:
            case DeploymentMode.LOCAL | DeploymentMode.SERVER:
                return "localhost"
            case DeploymentMode.DOCKER:
                return "mongodb"
            case _:
                return "localhost"