

from src.actions.questions.question import Question
from src.actions.answeres.yesNoAnswere import YesNoAnswere


class KillHitlerQuestion(Question):

    def __init__(self) -> None:
        super().__init__(YesNoAnswere)

    def getResult(self) -> bool:
        if self.result.Answere == "Yes":
            return True