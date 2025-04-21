from src.enums.controllerType import ControllerType


class ControllerTypeInvalidException(Exception):

    def __init__(self, controllerName: str):
        self.message = f"The ControllerType <{controllerName}> does not exist. Available are: {', '.join(controllerType.value for controllerType in ControllerType)}"
        super().__init__(self.message)