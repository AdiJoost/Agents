

from pydantic import BaseModel


class Question():

    PROMPT = ""

    def __init__(self, answereFormat: BaseModel) -> None:
        self.answereFormat = answereFormat
        self.result = ""

    def getAnswereSchema(self) -> BaseModel:
        return self.answereFormat
    
    def setResult(self, response) -> None:
        self.result = self.answereFormat.model_validate_json(response.message.content)

    def getValue(self) -> str:
        return self.result.Answere

    def getResult(self) -> any:
        return self.getValue()
    
    def getPrompt(self) -> str:
        return self.PROMPT