from enum import Enum

class DeploymentMode(Enum):
    LOCAL = "local"
    SERVER = "server"
    DOCKER = "docker"