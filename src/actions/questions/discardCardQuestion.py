from typing import List
from log.logger import Logger
from src.actions.answeres.yesNoAnswere import StringAnswere
from src.actions.questions.question import Question
from src.enums.policy import Policy


class DiscardCardQuestion(Question):
    PROMPT = "You have to discard one policy. Answere only with 'fascist' or 'liberal'."

    def __init__(self) -> None:
        super().__init__(StringAnswere)
        self.logger = Logger()

    def getResult(self, possibleOptions: List[Policy]) -> Policy:
        choosenPolicy = self._getPolicyEnum(self.getValue().strip().lower())
        if choosenPolicy in possibleOptions:
            return choosenPolicy
        self.logger.warn(f"The choosen policy is not in the options: {self.getValue()} Return other policy")
        return Policy.LIBERAL if choosenPolicy == Policy.FASCIST else Policy.FASCIST
    
    def _getPolicyEnum(self, choosenPolicy) -> Policy:
        if (choosenPolicy == Policy.LIBERAL):
            return Policy.LIBERAL
        return Policy.FASCIST
    
    def getPrompt(self, options: List[Policy]):
        optionsPrompt = f"You have drawn the cards: {','.join(options)}. {self.PROMPT}"
        return super().getPrompt()