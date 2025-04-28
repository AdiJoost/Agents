

import random
from typing import List
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
from src.models.thoughtsModel import ThoughtsModel
from src.simulation.gamestate import GameState


class BaseAgent():

    def __init__(self, agentName:str, agentRole: str, agentRoleDescription: str, agentInstructions: str, model:str, useReflection: bool, useReasoning: bool, promptManager: PromptManager) -> None:
        self.agentName = agentName
        self.agentRole = agentRole
        self.promptManager = promptManager
        self.agentInstructions = agentInstructions
        self.llmController = LLM_Controller(model=model)
        self.thoughts: List[ThoughtsModel] = []
        self.logger = Logger()
        self.gameState = None
        self.useReasoning = useReasoning
        self.useReflection = useReflection
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
        for thought in self.thoughts:
            thought.save()

    def setGameState(self, gameState: GameState) -> None:
        self.gameState = gameState

    def _thinkAndAnswere(self, args: dict):
        prompt = args.get(PromptMessages.RECENT_MESSAGES, "")
        messages = []
        self._addInstructionsAndPastMessages(messages, prompt)
        self._reason(messages=messages)
        messages.append({"role": "user", "content": "Based on your thought and everything that has been said, give an answere to the table to reach your goal. Only respond with what you would say to others playing on the table."})
        self._reflect(messages=messages)
        return self.llmController.generateOnMessage(messages)

    def _discardOneCard(self, args: dict):
        prompt = args.get(PromptMessages.DISCARD_ONE_CARD, "Choose a card to throw away.")
        options = args.get(PromptMessages.CARDS_AVAILABEL, [])
        # Check here for not empty list
        messages = []
        self._addInstructionsAndPastMessages(messages, prompt)
        self._reason(messages=messages)
        messages.append({"role": "user", "content": DiscardCardQuestion().getPrompt(options)})
        messages.append({"role": "user", "content": f"You're options are: {options}"})
        answere: DiscardCardQuestion = self.llmController.generateAnswere(messages=messages, question=DiscardCardQuestion())
        self._reflect(messages=messages)
        return answere.getResult(options)
 
    def _voteForKPresident(self, args: dict):
        prompt = args.get("prompt", "Answere yes or no")
        messages = []
        self._addInstructionsAndPastMessages(messages, prompt)
        self._reason(messages=messages)
        messages.append({"role": "user", "content": YesNoQuestion().getPrompt()})
        self._reflect(messages=messages)
        return self.llmController.generateAnswere(messages=messages, question=YesNoQuestion())
    
    def _chooseChancellorCandidate(self, args: dict):
        prompt = args.get(PromptMessages.CHOOSE_A_CHANCELLOR_CANDIDATE, "Choose a name")
        options = args.get(PromptMessages.CHANCELLOR_OPTIONS, [])
        # Check here for not empty list
        messages = []
        self._addInstructionsAndPastMessages(messages, prompt)
        messages.append({"role": "user", "content": ChooseChancellorQuestion().getPrompt()})
        messages.append({"role": "user", "content": f"You're options are: {options}"})
        self._reason(messages=messages)
        for _ in range(3):
            answere: ChooseChancellorQuestion = self.llmController.generateAnswere(messages=messages, question=ChooseChancellorQuestion())
            candidate = answere.getResult(possibleOptions=options)
            if candidate:
                self._reason(messages=messages)
                return candidate
        self.logger.warn(f"Player {self.agentName} was unable to choose a correct chancellor candidate. Choosing at random")
        return random.choice(options)
    
    def _addInstructionsAndPastMessages(self, messages: list, prompts: str) -> None:
        messages.append({"role": "user", "content": self.agentInstructions})
        messages.append({"role": "user", "content": prompts})

    def _reason(self, messages: list) -> None:
        if self.useReasoning:  
            messages.append({"role": "user", "content": "Think about what strategy you could use and formulate a tip for yourself."})
            reasoning = self.llmController.generateOnMessage(messages)
            self.thoughts.append(
                                ThoughtsModel(
                                    agentName=self.agentName,
                                    time=self.gameState.getTime(),
                                    message=f"My tip: {reasoning}",
                                    gameId=self.gameState.getGameId()
                                )
                )
            messages.append({"role": "user", "content": "[A tip]: {reasoning}"})

    def _reflect(self, messages: list) -> None:
        if self.useReflection:
            messages.append({"role": "user", "content": "Reflect on the tip for this situation of the game."})
            reflection = self.llmController.generateOnMessage(messages)
            self.thoughts.append(
                ThoughtsModel(
                    agentName=self.agentName,
                    time=self.gameState.getTime(),
                    message=reflection,
                    gameId=self.gameState.getGameId()
                )
            )
    