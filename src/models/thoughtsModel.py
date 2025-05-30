from bson.objectid import ObjectId
from src.models.baseModel import BaseModel


class ThoughtsModel(BaseModel):

    COLLECTION_NAME = "thought"

    def __init__(self, agentName: str, time: int, message: str, gameId: ObjectId, _id: ObjectId=None) -> None:
        self._id = _id
        self.agentName = agentName
        self.time = time
        self.message = message
        self.gameId = gameId

    def getMessage(self) -> str:
        return self.message
    
    def setMessage(self, message: str) -> None:
        self.message = message
    
    def getAgentName(self) -> str:
        return self.getAgentName
    
    def setAgentName(self, agentName:str) -> None:
        self.agentName = agentName

    def getTime(self) -> int:
        return self.time
    
    def setTime(self, time:int) -> None:
        self.time = time

    def toJson(self) -> dict:
        values = {
            "agentName": self.agentName,
            "time": self.time,
            "message": self.message,
            "gameId": str(self.gameId)
        }
        return self.addIdToJson(values)