

from log.logger import Logger
from src.actions.questions.question import Question
from src.actions.answeres.yesNoAnswere import StringAnswere


class YesNoQuestion(Question):

    PROMPT = "answere just with 'yes' or 'no'"

    def __init__(self) -> None:
        super().__init__(StringAnswere)
        self.logger = Logger()

    def getResult(self) -> bool:
        if self.getValue().strip().lower() == "yes":
            return True
        if self.getValue().strip().lower() == "no":
            return False
        self.logger.warn(f"A yes or no Aswere was aswered with: {self.result.Answere} Return default No")
        return False
        