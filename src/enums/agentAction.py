from enum import Enum, auto

class AgentAction(Enum):
    THINK_AND_ANSWERE = auto()
    VOTE_FOR_KILLING = auto()
    CHOOSE_CHANCELLOR_CANDIDATE = auto()