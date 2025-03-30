

import random
from log.logger import Logger
from src.actions.questions.chooseChancellorQuestion import ChooseChancellorQuestion
from src.actions.questions.yesNoQuestion import YesNoQuestion
from src.enums.agentAction import AgentAction
from src.enums.promptMessages import PromptMessages
from src.llmController.llm_controller import LLM_Controller


class BaseAgent():

    def __init__(self, agentName:str, agentRole: str, agentRoleDescription: str, agentInstructions: str, model:str) -> None:
        # Maybe needs more fields.
        self.agentName = agentName
        self.agentRole = agentRole
        self.agentRoleDescription = agentRoleDescription
        self.agentInstructions = agentInstructions
        self.llmController = LLM_Controller(model=model)
        self.logger = Logger()

    def action(self, action: AgentAction, args: dict = {}) -> any:
        match action:
            case AgentAction.THINK_AND_ANSWERE:
                return self._thinkAndAnswere(args)
            case AgentAction.VOTE_FOR_KILLING:
                return self._voteForKilling(args)
            case AgentAction.CHOOSE_CHANCELLOR_CANDIDATE:
                return self._chooseChancellorCandidate(args)
            case _:
                self.logger.error(f"Action <{action}> not implemented")
        
    def _thinkAndAnswere(self, args: dict):
        prompt = args.get("prompt") if args.get("prompt") else "What do you like to do?"
        return self._think(prompt)

    def _think(self, prompt: str) -> None:
        messages = []
        messages.append({"role": "user", "content": self.agentInstructions})
        messages.append({"role": "user", "content": prompt})
        return self.llmController.generateOnMessage(messages)
    
    def _voteForKilling(self, args: dict):
        prompt = args.get("prompt", "Answere yes or no")
        messages = []
        messages.append({"role": "user", "content": self.agentInstructions})
        messages.append({"role": "user", "content": prompt})
        return self.llmController.generateAnswere(messages=messages, question=YesNoQuestion())
    
    def _chooseChancellorCandidate(self, args: dict):
        prompt = args.get(PromptMessages.CHOOSE_A_CHANCELLOR_CANDIDATE, "Choose a name")
        options = args.get(PromptMessages.CHANCELLOR_OPTIONS, [])
        # Check here for not empty list
        messages = []
        messages.append({"role": "user", "content": self.agentInstructions})
        messages.append({"role": "user", "content": prompt})
        messages.append({"role": "user", "content": f"You're options are: {options}"})
        for _ in range(3):
            answere: ChooseChancellorQuestion = self.llmController.generateAnswere(messages=messages, question=ChooseChancellorQuestion())
            candidate = answere.getResult(possibleOptions=options)
            if candidate:
                return candidate
        self.logger.warn(f"Player {self.agentName} was unable to choose a correct chancellor candidate. Choosing at random")
        return random.choice(options)

