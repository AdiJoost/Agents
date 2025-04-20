

from src.enums.policy import Policy


class GameState():

    def __init__ (self, policiesForBadWins: int = 6, policiesForGoodWins: int = 5, badPoliciesUntilHitlerWins: int = 2, killingNumbers: list = [3,4], inspectingNumbers: list = [2]) -> None:
        self.policiesForBadWins = policiesForBadWins
        self.policiesForGoodWins = policiesForGoodWins
        self.badPoliciesUntilHitlerWins = badPoliciesUntilHitlerWins
        self.killingNumbers = killingNumbers
        self.inspectingNumbers = inspectingNumbers
        self.badPoliciesPlayed = 0
        self.goodPoliciesPlayed = 0

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
    
    def getGameStatePrompt(self) -> str:
        return f"On the Board are {self.goodPoliciesPlayed} liberal cards played and {self.badPoliciesPlayed} fascist cards played."
