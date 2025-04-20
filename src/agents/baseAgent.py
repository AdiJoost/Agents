

import random
from data.dataManagers.enums.promptFiles import PromptFiles
from data.dataManagers.realization.promptManager import PromptManager
from data.dataManagers.realization.txtManager import TxtManager
from log.logger import Logger
from src.actions.questions.chooseChancellorQuestion import ChooseChancellorQuestion
from src.actions.questions.discardCardQuestion import DiscardCardQuestion
from src.actions.questions.yesNoQuestion import YesNoQuestion
from src.enums.agentAction import AgentAction
from src.enums.promptMessages import PromptMessages
from src.llmController.llm_controller import LLM_Controller


class BaseAgent():

    def __init__(self, agentName:str, agentRole: str, agentRoleDescription: str, agentInstructions: str, model:str, useReflection: bool, useReasoning: bool, promptManager: PromptManager) -> None:
        self.agentName = agentName
        self.agentRole = agentRole
        self.promptManager = promptManager
        self.agentRoleDescription = agentRoleDescription
        self.agentInstructions = agentInstructions
        self.llmController = LLM_Controller(model=model)
        self.useReasoning = useReasoning
        self.useReflection = useReflection
        self.thoughts = []
        self.logger = Logger()
        self.protocolLogger = TxtManager(f"thoughts_{agentName}", "discussions/agentThoughts")

    def setHitler(self) -> None:
        self.agentRole = self.promptManager.getPrompt(PromptFiles.HITLER_ROLE_DESCRIPTION)

    def setFascist(self) -> None:
        self.agentRole = self.promptManager.getPrompt(PromptFiles.FASCIST_ROLE_DESCRIPTION)

    def setLiberal(self) -> None:
        self.agentRole = self.promptManager.getPrompt(PromptFiles.LIBERAL_ROLE_DESCRIPTION)

    def action(self, action: AgentAction, args: dict = {}) -> any:
        match action:
            case AgentAction.THINK_AND_ANSWERE:
                return self._thinkAndAnswere(args)
            case AgentAction.VOTE_FOR_KILLING:
                return self._voteForKPresident(args)
            case AgentAction.CHOOSE_CHANCELLOR_CANDIDATE:
                return self._chooseChancellorCandidate(args)
            case AgentAction.DISCARD_ONE_CARD:
                return self._discardOneCard(args)
            case _:
                self.logger.error(f"Action <{action}> not implemented")

    def logProtocol(self) -> None:
        if (self.protocolLogger):
            self.protocolLogger.writeLine(f"Instructions for {self.agentName}:")
            self.protocolLogger.writeLine(self.agentInstructions)
            self.protocolLogger.writeLine(f"Thougths of {self.agentName}")
            for entry in self.thoughts:
                self.protocolLogger.writeLine(entry)
                self.protocolLogger.writeLine("---")

    def _thinkAndAnswere(self, args: dict):
        prompt = args.get(PromptMessages.RECENT_MESSAGES, "")
        messages = []
        self._addInstructionsAndPastMessages(messages, prompt)
        messages.append({"role": "user", "content": "Based on your thought and everything that has been said, give an answere to the table to reach your goal. Only respond with what you would say to others playing on the table."})
        return self.llmController.generateOnMessage(messages)

    def _discardOneCard(self, args: dict):
        prompt = args.get(PromptMessages.DISCARD_ONE_CARD, "Choose a card to throw away.")
        options = args.get(PromptMessages.CARDS_AVAILABEL, [])
        # Check here for not empty list
        messages = []
        self._addInstructionsAndPastMessages(messages, prompt)
        messages.append({"role": "user", "content": DiscardCardQuestion().getPrompt(options)})
        messages.append({"role": "user", "content": f"You're options are: {options}"})
        answere: DiscardCardQuestion = self.llmController.generateAnswere(messages=messages, question=DiscardCardQuestion())
        return answere.getResult(options)
 
    def _voteForKPresident(self, args: dict):
        prompt = args.get("prompt", "Answere yes or no")
        messages = []
        self._addInstructionsAndPastMessages(messages, prompt)
        messages.append({"role": "user", "content": YesNoQuestion().getPrompt()})
        return self.llmController.generateAnswere(messages=messages, question=YesNoQuestion())
    
    def _chooseChancellorCandidate(self, args: dict):
        prompt = args.get(PromptMessages.CHOOSE_A_CHANCELLOR_CANDIDATE, "Choose a name")
        options = args.get(PromptMessages.CHANCELLOR_OPTIONS, [])
        # Check here for not empty list
        messages = []
        self._addInstructionsAndPastMessages(messages, prompt)
        messages.append({"role": "user", "content": ChooseChancellorQuestion().getPrompt()})
        messages.append({"role": "user", "content": f"You're options are: {options}"})
        for _ in range(3):
            answere: ChooseChancellorQuestion = self.llmController.generateAnswere(messages=messages, question=ChooseChancellorQuestion())
            candidate = answere.getResult(possibleOptions=options)
            if candidate:
                return candidate
        self.logger.warn(f"Player {self.agentName} was unable to choose a correct chancellor candidate. Choosing at random")
        return random.choice(options)
    
    def _addInstructionsAndPastMessages(self, messages: list, prompts: str) -> None:
        messages.append({"role": "user", "content": self.agentInstructions})
        if self.useReasoning or self.useReflection:
            messages.append({"role": "user", "content": f"These are your past thoughts: {','.join(self.thoughts)}"})
        messages.append({"role": "user", "content": prompts})
        self._reason(messages)
        self._reflect(messages)

    def _reason(self, messages: list) -> None:
        if self.useReasoning:  
            messages.append({"role": "user", "content": "Based on what has been said, your role in this game and the state of the game, think about what would be the best steps to archive your goals."})
            reasoning = self.llmController.generateOnMessage(messages)
            self.thoughts.append(f"My reasoning: {reasoning}")
            messages.append({"role": "user", "content": "Your reflection is: {reasoning}"})

    def _reflect(self, messages: list) -> None:
        if self.useReflection:
            messages.append({"role": "user", "content": "Reflect on the actions you decided to take."})
            reflection = self.llmController.generateOnMessage(messages)
            self.thoughts.append(f"My reflection: {reflection}")
            messages.append({"role": "user", "content": "Your reflection is: {reflection}"})
    