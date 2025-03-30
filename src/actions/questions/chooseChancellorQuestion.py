

from typing import List
from log.logger import Logger
from src.actions.questions.question import Question
from src.actions.answeres.yesNoAnswere import StringAnswere


class ChooseChancellorQuestion(Question):

    def __init__(self) -> None:
        super().__init__(StringAnswere)
        self.logger = Logger()

    def getResult(self, possibleOptions: List[str]) -> bool:
        choosenName =  self.getValue().strip().lower()
        normalizedOptions = [name.strip().lower() for name in possibleOptions]
        if choosenName in normalizedOptions:
            return choosenName
        self.logger.warn(f"The choosen chancellor is not playing: {self.getValue()} Return None")
        return None