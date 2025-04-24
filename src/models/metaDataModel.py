

from src.models.baseModel import BaseModel


class MetaDataModel(BaseModel):

    COLLECTION_NAME = "meta_data_model"

    def __init__(self, agents, timeStarted, timeEnded, result:str, _id = None) -> None:
        self._id = _id
        self.agents = agents
        self.timeStarted = timeStarted
        self.timeEnded = timeEnded
        self.result = result

    def getAgents (self)->any:
        return self.agents
    
    def setAgents(self, agents: any) -> None:
        self.agents = agents

    def getTimeStarted (self) -> any:
        return self.timeStarted
    
    def setTimeStarted (self, timeStarted) -> None:
        self.timeStarted = timeStarted

    def getTimeEnded (self) -> any:
        return self.timeEnded
    
    def setTimeEnded(self, timeEnded) -> None:
        self.timeEnded = timeEnded

    def getResult(self) -> str:
        return self.result
    
    def setResult(self, result: str) -> None:
        self.result = result 

    def toJson(self) -> dict:
        values = {
            "agents": self.agents,
            "timeStarted": self.timeStarted,
            "timeEnded": self.timeEnded,
            "result": self.result
        }
        return self.addIdToJson(values)