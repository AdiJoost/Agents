

from typing import List

from config.simulationConfig.simulationManager import SimulationManager
from data.dataManagers.realization.txtManager import TxtManager
from src.actions.questions.killHittlerQuestion import KillHitlerQuestion
from src.agents.baseAgent import BaseAgent
from src.enums.agentAction import AgentAction


class BaseSimulation():

    def __init__(self, simulationManager: SimulationManager, protocolLogger: TxtManager=None) -> None:
        self.simulationManager = simulationManager
        self.protocolLogger = protocolLogger
        self.agents: List[BaseAgent] = self.simulationManager.getAgents()
        self.protocol = [self.simulationManager.getInitialPrompt()]

    def run(self) -> None:
        self._simulateStep()
        self._voteForKilling()
        self._logProtocol()
            
        
    def _simulateStep(self) -> None:
        for agent in self.agents:
            everythingSaid = self._getEverythingSaid()
            self.protocol.append(f"{agent.agentName}: {agent.action(AgentAction.THINK_AND_ANSWERE, {"prompt": f"What has been told on the table so far: {everythingSaid}"})}")

    def _voteForKilling(self):
        self.protocol.append(f"Question: {self.simulationManager.getQuestion()}")
        kills = 0
        lives = 0
        everythinSaid = self._getEverythingSaid()
        for agent in self.agents:
            agentResponse = agent.action(AgentAction.VOTE_FOR_KILLING, {"prompt": f"What has been told on the table so far: {everythinSaid}"})
            if isinstance(agentResponse, KillHitlerQuestion):
                if agentResponse.getResult():
                    kills += 1
                else:
                    lives += 1
        self.protocol.append(f"Result of Voting: Kill: {kills}, lives: {lives}")
                                         

    def _getEverythingSaid(self) -> str:
        return ",".join(f"[{answere}]" for answere in self.protocol)

    def _logProtocol(self) -> None:
        if (self.protocolLogger):
            self.protocolLogger.writeLine("Result")
            for entry in self.protocol:
                self.protocolLogger.writeLine(entry)
                self.protocolLogger.writeLine("---")

