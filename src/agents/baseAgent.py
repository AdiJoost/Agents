

import random
from data.dataManagers.realization.txtManager import TxtManager
from log.logger import Logger
from src.actions.questions.chooseChancellorQuestion import ChooseChancellorQuestion
from src.actions.questions.yesNoQuestion import YesNoQuestion
from src.enums.agentAction import AgentAction
from src.enums.promptMessages import PromptMessages
from src.llmController.llm_controller import LLM_Controller


class BaseAgent():

    def __init__(self, agentName:str, agentRole: str, agentRoleDescription: str, agentInstructions: str, model:str) -> None:
        self.agentName = agentName
        self.agentRole = agentRole
        self.agentRoleDescription = agentRoleDescription
        self.agentInstructions = agentInstructions
        self.llmController = LLM_Controller(model=model)
        self.thoughts = []
        self.logger = Logger()
        self.protocolLogger = TxtManager(f"thoughts_{agentName}", "discussions/agentThoughts")

    def setHitler(self) -> None:
        self.agentRole = "You are the Leader of the Bad guys in this game. You try to lie and want to play red cards."

    def setFascist(self) -> None:
        self.agentRole = "You are a suporter of the bad guys. You try to lie and want to play red cards or get your leader to be elected."

    def setLiberal(self) -> None:
        self.agentRole = "You are a good guy. You want to find out, who on the table is a bad guy and want to play blue cards"


    def action(self, action: AgentAction, args: dict = {}) -> any:
        match action:
            case AgentAction.THINK_AND_ANSWERE:
                return self._thinkAndAnswere(args)
            case AgentAction.VOTE_FOR_KILLING:
                return self._voteForKPresident(args)
            case AgentAction.CHOOSE_CHANCELLOR_CANDIDATE:
                return self._chooseChancellorCandidate(args)
            case _:
                self.logger.error(f"Action <{action}> not implemented")

    def logProtocol(self) -> None:
        if (self.protocolLogger):
            self.protocolLogger.writeLine(f"Thougths of {self.agentName}")
            for entry in self.thoughts:
                self.protocolLogger.writeLine(entry)
                self.protocolLogger.writeLine("---")
        
    def _thinkAndAnswere(self, args: dict):
        prompt = args.get(PromptMessages.RECENT_MESSAGES, "")
        messages = []
        messages.append({"role": "user", "content": self.agentInstructions})
        messages.append({"role": "user", "content": prompt})
        messages.append({"role": "user", "content": self._reason(messages)})
        messages.append({"role": "user", "content": self._reflect(messages)})
        messages.append({"role": "user", "content": "Based on your thought, give an answere to the table"})
        return self.llmController.generateOnMessage(messages)
    
    def _reason(self, messages: list) -> None:  
        messages.append({"role": "user", "content": "Based on what has been said, your role in this game and the state of the game, think about what would be the best steps to archive your goals."})
        reasoning = self.llmController.generateOnMessage(messages)
        self.thoughts.append(f"My reasoning: {reasoning}")
        return reasoning

    def _reflect(self, messages: list) -> None:
        messages.append({"role": "user", "content": "Reflect on the actions you decided to take."})
        reflection = self.llmController.generateOnMessage(messages)
        self.thoughts.append(f"My reflection: {reflection}")
        return reflection
    
    def _voteForKPresident(self, args: dict):
        prompt = args.get("prompt", "Answere yes or no")
        messages = []
        messages.append({"role": "user", "content": self.agentInstructions})
        messages.append({"role": "user", "content": prompt})
        messages.append({"role": "user", "content": self._reason(messages)})
        messages.append({"role": "user", "content": self._reflect(messages)})
        messages.append({"role": "user", "content": YesNoQuestion.getPrompt()})
        return self.llmController.generateAnswere(messages=messages, question=YesNoQuestion())
    
    def _chooseChancellorCandidate(self, args: dict):
        prompt = args.get(PromptMessages.CHOOSE_A_CHANCELLOR_CANDIDATE, "Choose a name")
        options = args.get(PromptMessages.CHANCELLOR_OPTIONS, [])
        # Check here for not empty list
        messages = []
        messages.append({"role": "user", "content": self.agentInstructions})
        messages.append({"role": "user", "content": f"You are about to choose an Chancellor. Your options are {options}"})
        messages.append({"role": "user", "content": f"You're options are: {options}"})
        messages.append({"role": "user", "content": self._reason(messages)})
        messages.append({"role": "user", "content": self._reflect(messages)})
        messages.append({"role": "user", "content": prompt})
        messages.append({"role": "user", "content": ChooseChancellorQuestion.getPrompt()})
        for _ in range(3):
            answere: ChooseChancellorQuestion = self.llmController.generateAnswere(messages=messages, question=ChooseChancellorQuestion())
            candidate = answere.getResult(possibleOptions=options)
            if candidate:
                return candidate
        self.logger.warn(f"Player {self.agentName} was unable to choose a correct chancellor candidate. Choosing at random")
        return random.choice(options)


