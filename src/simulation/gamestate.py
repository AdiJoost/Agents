

from typing import List
from src.enums.policy import Policy
from src.models.messageModel import MessageModel


class GameState():

    def __init__ (self, policiesForBadWins: int = 6, policiesForGoodWins: int = 5, badPoliciesUntilHitlerWins: int = 2, killingNumbers: list = [3,4], inspectingNumbers: list = [2]) -> None:
        self.policiesForBadWins = policiesForBadWins
        self.policiesForGoodWins = policiesForGoodWins
        self.badPoliciesUntilHitlerWins = badPoliciesUntilHitlerWins
        self.killingNumbers = killingNumbers
        self.inspectingNumbers = inspectingNumbers
        self.badPoliciesPlayed = 0
        self.goodPoliciesPlayed = 0
        self.gameProtocol: List[MessageModel] = []

    def playPolicy (self, policy: Policy) -> None:
        if policy == Policy.LIBERAL:
            self.goodPoliciesPlayed += 1
        self.badPoliciesPlayed += 1

    def haveBadPeopleWon (self, hitlerIsElectedCancelor: bool) -> bool:
        if self.badPoliciesPlayed >= self.badPoliciesUntilHitlerWins and hitlerIsElectedCancelor:
            return True
        if self.badPoliciesPlayed >= self.policiesForBadWins:
            return True
        return False
    
    def haveGoodPeopleWon(self) -> bool:
        return self.goodPoliciesPlayed >= self.policiesForGoodWins
    
    def presidentCanShoot(self, policyPlayed: Policy) -> bool:
        if policyPlayed == Policy.LIBERAL:
            return False
        return self.badPoliciesPlayed in self.killingNumbers
    
    def presidentCanInspect(self, policyPlayed: Policy) -> bool:
        if policyPlayed == Policy.LIBERAL:
            return False
        return self.badPoliciesPlayed in self.inspectingNumbers
    
    def addMessage(self, message: MessageModel) -> None:
        self.gameProtocol.append(message)

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
