

import random
from typing import List

from config.simulationConfig.simulationManager import SimulationManager
from data.dataManagers.realization.txtManager import TxtManager
from log.logger import Logger
from src.actions.questions.yesNoQuestion import YesNoQuestion
from src.agents.baseAgent import BaseAgent
from src.enums.agentAction import AgentAction
from src.enums.promptMessages import PromptMessages


class BaseSimulation():

    def __init__(self, simulationManager: SimulationManager, protocolLogger: TxtManager=None) -> None:
        self.simulationManager = simulationManager
        self.protocolLogger = protocolLogger
        self.gameStateLogger = Logger(filename = "gamestate")
        self.agents: List[BaseAgent] = self.simulationManager.getAgents()
        self._assignGameRoles()
        self.protocol = [self.simulationManager.getInitialPrompt()]
        self.presidentCandidatePosition = 0
        self.chancellorCandidateName = None
        self.presidentCandidate: BaseAgent = self.agents[0]

    def _assignGameRoles(self) -> None:
        numberOfFacists = self.simulationManager.getNumberOfFacists()
        if numberOfFacists + 1 >= len(self.agents):
            raise ValueError(f"There are more Roles to assign ({numberOfFacists + 1}) than people ({len(self.agents)}) on the table.")
        badGuys = random.sample(self.agents, numberOfFacists + 1)
        for agent in badGuys:
            agent.setFascist()
        badGuys[0].setHitler()
        for agent in [agent for agent in self.agents if agent not in badGuys]:
            agent.setLiberal()

    def run(self) -> None:
        self.gameStateLogger.info("Set new president.")
        self._setPresidentCandidate()
        self.gameStateLogger.info("Simulate Step")
        self._simulateStep()
        self.gameStateLogger.info("Choosing new ChancellorCandidate")
        self._askPresidentForChancellorCandidate()
        self.gameStateLogger.info("Simulate Step")
        self._simulateStep()
        self.gameStateLogger.info(f"Vote for President {self.presidentCandidate.agentName} and chancellor {self.chancellorCandidateName}")
        self._voteForPresident()
        self.gameStateLogger.info(f"Simulation ended. Generating Protocol")
        self._logProtocol()
            
        
    def _simulateStep(self) -> None:
        for agent in self.agents:
            everythingSaid = self._getEverythingSaid()
            self.gameStateLogger.info(f"Asking {agent.agentName} for input")
            self.protocol.append(f"{agent.agentName}: {agent.action(AgentAction.THINK_AND_ANSWERE, {PromptMessages.RECENT_MESSAGES: f"What has been told on the table so far: {everythingSaid}"})}")

    def _voteForPresident(self):
        self.protocol.append(f"Question: {self.simulationManager.getQuestion()}")
        yes = 0
        no = 0
        everythinSaid = self._getEverythingSaid()
        for agent in self.agents:
            self.gameStateLogger.info(f"Asking {agent.agentName} for Vote")
            agentResponse = agent.action(AgentAction.VOTE_FOR_KILLING, {PromptMessages.RECENT_MESSAGES: f"What has been told lately: {everythinSaid}"})
            if isinstance(agentResponse, YesNoQuestion):
                if agentResponse.getResult():
                    yes += 1
                    self.protocol.append(f"{agent.agentName} voted yes")
                else:
                    no += 1
                    self.protocol.append(f"{agent.agentName} voted no")
        self.protocol.append(f"Result of Voting for {self.presidentCandidate.agentName}: Yes: {yes}, No: {no}")
                                         
    def _setPresidentCandidate(self) -> None:
        if (self.presidentCandidatePosition >= len(self.agents)):
            self.presidentCandidatePosition = 0
        self.presidentCandidate = self.agents[self.presidentCandidatePosition]
        self.presidentCandidatePosition += 1

    def _askPresidentForChancellorCandidate(self) -> None:
        candidates = self._getChancellorCandidates()
        args = {}
        args[PromptMessages.EVERYTHING_SAID] = self._getEverythingSaid()
        args[PromptMessages.CHOOSE_A_CHANCELLOR_CANDIDATE] = "You are the president, you have to choose your chanellor candidate on this table. Answere only with their name."
        args[PromptMessages.CHANCELLOR_OPTIONS] = candidates
        self.chancellorCandidateName = self.presidentCandidate.action(AgentAction.CHOOSE_CHANCELLOR_CANDIDATE, args=args)
        
        self.protocol.append(f"{self.presidentCandidate.agentName} is the president candidate, they have choosen {self.chancellorCandidateName} as their channcellor candidate")

    def _getChancellorCandidates(self) -> None:
        return [agent.agentName for agent in self.agents if agent.agentName != self.presidentCandidate.agentName]


    def _getEverythingSaid(self) -> str:
        return ",".join(f"[{answere}]" for answere in self.protocol)

    def _logProtocol(self) -> None:
        for agent in self.agents:
            agent.logProtocol()
        if (self.protocolLogger):
            self.protocolLogger.writeLine("Result")
            for entry in self.protocol:
                self.protocolLogger.writeLine(entry)
                self.protocolLogger.writeLine("---")

