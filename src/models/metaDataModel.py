

from src.models.baseModel import BaseModel


class MetaDataModel(BaseModel):

    COLLECTION_NAME = "meta_data_model"

    def __init__(self, agents, timeStarted, timeEnded, resultId=1, _id = None) -> None:
        self._id = _id
        self.agents = agents
        self.timeStarted = timeStarted
        self.timeEnded = timeEnded
        self.resultId = resultId

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

    def toJson(self) -> dict:
        values = {
            "agents": self.agents,
            "timeStarted": self.timeStarted,
            "timeEnded": self.timeEnded
        }
        return self.addIdToJson(values)