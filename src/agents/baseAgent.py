

from src.enums.agentAction import AgentAction


class BaseAgent():

    def __init__(self, name:str) -> None:
        # Maybe needs more fields.
        self.name = name

    def action(self, action: AgentAction, args: dict = {}) -> any:
        #execute the action with possible many args and return the desired object.
        pass

    def _think(self) -> None:
        #let the agent think. Maybe later, it can do different actions like reflect, reason etc. But we have to reasearch this.
        pass
