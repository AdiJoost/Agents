

from typing import List, Union
from src.enums.policy import Policy
from src.enums.winingReason import WiningReason
from src.models.messageModel import MessageModel


class GameState():

    def __init__ (self, gameId: str, policiesForBadWins: int = 6, policiesForGoodWins: int = 5, badPoliciesUntilHitlerWins: int = 2, killingNumbers: list = [3,4], inspectingNumbers: list = [2]) -> None:
        self.gameId = gameId
        self.policiesForBadWins = policiesForBadWins
        self.policiesForGoodWins = policiesForGoodWins
        self.badPoliciesUntilHitlerWins = badPoliciesUntilHitlerWins
        self.killingNumbers = killingNumbers
        self.inspectingNumbers = inspectingNumbers
        self.badPoliciesPlayed = 0
        self.goodPoliciesPlayed = 0
        self.gameProtocol: List[MessageModel] = []
        self.time = 0

    def playPolicy (self, policy: Policy) -> None:
        if policy == Policy.LIBERAL:
            self.goodPoliciesPlayed += 1
        self.badPoliciesPlayed += 1

    def isGameOver(self, hitlerIsElectedCancelor: bool) -> Union[str, None]:
        if self.haveBadPeopleWon(hitlerIsElectedCancelor=hitlerIsElectedCancelor) is not None:
            return self.haveBadPeopleWon(hitlerIsElectedCancelor=hitlerIsElectedCancelor)
        if self.haveGoodPeopleWon() is not None:
            return self.haveGoodPeopleWon()
        return None

    def haveBadPeopleWon (self, hitlerIsElectedCancelor: bool) -> Union[str, None]:
        if self.badPoliciesPlayed >= self.badPoliciesUntilHitlerWins and hitlerIsElectedCancelor:
            return WiningReason.WON_BY_ELECTION
        if self.badPoliciesPlayed >= self.policiesForBadWins:
            return WiningReason.WON_BY_FASCIST_CARDS
        return None
    
    def haveGoodPeopleWon(self) -> Union[str, None]:
        if self.goodPoliciesPlayed >= self.policiesForGoodWins:
            return WiningReason.WON_BY_LIBERAL_CARDS
        return None
    
    def presidentCanShoot(self, policyPlayed: Policy) -> bool:
        if policyPlayed == Policy.LIBERAL:
            return False
        return self.badPoliciesPlayed in self.killingNumbers
    
    def presidentCanInspect(self, policyPlayed: Policy) -> bool:
        if policyPlayed == Policy.LIBERAL:
            return False
        return self.badPoliciesPlayed in self.inspectingNumbers
    
    def addMessage(self, message: MessageModel) -> None:
        message.setTime(self.time)
        self.gameProtocol.append(message)

    def increaseTime(self) -> None:
        self.time += 1

    def getTime(self) -> int:
        return self.time
    
    def getGameId(self) -> str:
        return self.gameId
    
    def setGameId(self, gameId: str) -> None:
        self.gameId = gameId

    def getMessage(self, numberOfPassedMessages: int) -> str:
        if numberOfPassedMessages < 1:
            return ""
        messages = self.gameProtocol[-numberOfPassedMessages:] if len(self.gameProtocol) > numberOfPassedMessages else self.gameProtocol
        returnValue = ""
        for message in messages:
            returnValue += f"-{message.agentName}-:{message.message}"
        return returnValue
    
    def saveMessages(self) -> None:
        for message in self.gameProtocol:
            message.save()
    
    def getGameStatePrompt(self) -> str:
        return f"On the Board are {self.goodPoliciesPlayed} liberal cards played and {self.badPoliciesPlayed} fascist cards played."
