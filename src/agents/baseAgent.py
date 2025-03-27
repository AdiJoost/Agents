

from src.actions.questions.killHittlerQuestion import KillHitlerQuestion
from src.enums.agentAction import AgentAction
from src.llmController.llm_controller import LLM_Controller


class BaseAgent():

    def __init__(self, agentName:str, agentRole: str, agentRoleDescription: str, agentInstructions: str, model:str) -> None:
        # Maybe needs more fields.
        self.agentName = agentName
        self.agentRole = agentRole
        self.agentRoleDescription = agentRoleDescription
        self.agentInstructions = agentInstructions
        self.llmController = LLM_Controller(model=model)

    def action(self, action: AgentAction, args: dict = {}) -> any:
        if action == AgentAction.THINK_AND_ANSWERE:
            return self._thinkAndAnswere(args)
        if action == AgentAction.VOTE_FOR_KILLING:
            return self._voteForKilling(args)
        
    def _thinkAndAnswere(self, args: dict):
        prompt = args.get("prompt") if args.get("prompt") else "What do you like to do?"
        return self._think(prompt)

    def _think(self, prompt: str) -> None:
        messages = []
        messages.append({"role": "user", "content": self.agentInstructions})
        messages.append({"role": "user", "content": prompt})
        return self.llmController.generateOnMessage(messages)
    
    def _voteForKilling(self, args: dict):
        prompt = args.get("prompt", "Answere Yes or no")
        messages = []
        messages.append({"role": "user", "content": self.agentInstructions})
        messages.append({"role": "user", "content": prompt})
        return self.llmController.generateAnswere(messages=messages, question=KillHitlerQuestion())

