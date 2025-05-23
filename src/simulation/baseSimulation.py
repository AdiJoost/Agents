

import random
from typing import List

from config.configFiles import ConfigFiles
from config.configManager import getConfig
from config.mongoDBConfig.mongoDbConfigFields import MongoDBConfigFields
from config.simulationConfig.simulationManager import SimulationManager
from data.dataManagers.realization.promptManager import PromptManager
from data.dataManagers.realization.txtManager import TxtManager
from log.logger import Logger
from src.actions.questions.yesNoQuestion import YesNoQuestion
from src.agents.baseAgent import BaseAgent
from src.enums.agentAction import AgentAction
from src.enums.policy import Policy
from src.enums.promptMessages import PromptMessages
from src.models.messageModel import MessageModel
from src.models.metaDataModel import MetaDataModel
from src.simulation.gamestate import GameState
from src.utils.serverConfig.serverConfig import ServerConfig


class BaseSimulation():

    def __init__(self, simulationManager: SimulationManager, protocolLogger: TxtManager=None, promptManager: PromptManager= PromptManager()) -> None:
        self.logDBConnection()
        self.simulationManager = simulationManager
        self.protocolLogger = protocolLogger
        self.promptManager = promptManager
        
        self.gameStateLogger = Logger(filename = "gamestate")
        self.agents: List[BaseAgent] = self.simulationManager.getAgents(self.promptManager)
        self._assignGameRoles()
        self.protocol = [self.simulationManager.getInitialPrompt()]
        self.presidentCandidatePosition = 0
        self.chancellorCandidateName = None
        self.presidentCandidate: BaseAgent = self.agents[0]
        self.chancellorCandidate: BaseAgent = self.agents[0]
        self.numberOfPassedMessages = self.simulationManager.getNumberOfPassedMessages()
        self.numberOfConsecutiveFailedElectrions = 0
        self.gameOver = False
        self.policyStack = self._getPolicyStack()
        self.drawnStack = []
        self.metaDataModel = MetaDataModel(agents=f"[{','.join([agent.agentName for agent in self.agents])}]", timeStarted=0, timeEnded=2, result=None)
        self.metaDataModel.save()
        self.gameId = self.metaDataModel.getId()
        self.gameState = GameState(
            policiesForBadWins = self.simulationManager.getNumberOfBadPoliciesForWin(),
            policiesForGoodWins = self.simulationManager.getNumberOfGoodPoliciesForWin(),
            gameId=self.gameId
        )
        for agent in self.agents:
            agent.setGameState(self.gameState)
        self._logSetup()

    def logDBConnection(self):
        logger = Logger()
        logger.info(ServerConfig.getMongoAddress())

    def _logSetup(self) -> None:
        self.gameStateLogger.info("Setup complete")
        for agent in self.agents:
            self.gameStateLogger.info(f"{agent.agentName} is in Role: <{agent.agentRole}>")

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

    def _getPolicyStack(self) -> List:
        policies = []
        for _ in range(self.simulationManager.getNumberOfLiberalPolicies()):
            policies.append(Policy.LIBERAL)
        for _ in range(self.simulationManager.getNumberOfFacistsPolicies()):
            policies.append(Policy.FASCIST)
        random.shuffle(policies)
        return policies

    def run(self) -> None:
        while not self.gameOver:
            self.gameStateLogger.info("Set new president.")
            self._setPresidentCandidate()
            self.gameStateLogger.info("Choosing new ChancellorCandidate")
            self._askPresidentForChancellorCandidate()
            self.gameStateLogger.info("Simulate Step")
            self._askForOpinions()
            self.gameStateLogger.info(f"Vote for President {self.presidentCandidate.agentName} and chancellor {self.chancellorCandidateName}")
            if self._voteForPresident():
                self.gameStateLogger.info("Get Policys")
                policyPlayed = self._getPolicy()
                self._addMessage(f"Policy {policyPlayed} got played by {self.presidentCandidate.agentName} and {self.chancellorCandidateName}.")
                self.protocol.append(f"Policy {policyPlayed} got played by {self.presidentCandidate.agentName} and {self.chancellorCandidateName}.")
                if policyPlayed == Policy.FASCIST:
                    self.gameState.playPolicy(policyPlayed)
                self._checkGameOver()
        self.gameStateLogger.info(f"Simulation ended. Generating Protocol")
        self._logProtocol()
        self.metaDataModel.setTimeEnded(self.gameState.getTime())
        self.metaDataModel.save()
        self.gameState.saveMessages()

    def _addMessage(self, message: str, agentName:str ="GameMaster") -> None:
        self.gameState.increaseTime()
        self.gameState.addMessage(MessageModel(
                    agentName=agentName,
                    message=message,
                    gameId=self.gameId
                ))

    def _checkGameOver(self) -> None:
        isGameOver = self.gameState.isGameOver(False)
        if isGameOver is not None:
            self.metaDataModel.setResult(isGameOver)
            self.gameOver = True

    def _getPolicy(self) -> Policy:
        drawnCards = self.policyStack[:3].copy()
        self.gameStateLogger.info(f"Policies drwan = {drawnCards}")
        self.policyStack = self.policyStack[3:]
        if len(self.policyStack) < 3:
            self.policyStack = self.policyStack + self.drawnStack
            random.shuffle(self.policyStack)
        argsForPresident = {}
        argsForPresident[PromptMessages.DISCARD_ONE_CARD] = f"You are president and draw three cards. You have to choose to discard one policy and give the other two to you Chancellor {self.chancellorCandidateName}"
        argsForPresident[PromptMessages.CARDS_AVAILABEL] = drawnCards.copy()
        self.gameStateLogger.info("Ask President for removal of card")
        target = self.presidentCandidate.action(AgentAction.DISCARD_ONE_CARD, args=argsForPresident)
        self.drawnStack.append(self._remove_first(drawnCards, target))
        self.gameStateLogger.info(f"President removed {target}")
        argsForChancellor = {}
        argsForChancellor[PromptMessages.DISCARD_ONE_CARD] = f"You are Chancellor and got two cards from {self.presidentCandidate.agentName}. You have to choose to discard one policy and play the other one one the table."
        argsForChancellor[PromptMessages.CARDS_AVAILABEL] = drawnCards.copy()
        self.gameStateLogger.info("Ask Chancellor for removal of card")
        target = self.chancellorCandidate.action(AgentAction.DISCARD_ONE_CARD, args=argsForChancellor)
        self.drawnStack.append(self._remove_first(drawnCards, target))
        self.gameStateLogger.info(f"Chancellor removed {target}")
        return drawnCards[0]
    
    def _remove_first(self, policies: List[Policy], target: Policy) -> Policy:
        for index, policy in enumerate(policies):
            if policy == target:
                del policies[index]
                return target
        self.gameStateLogger.warn("Policy wants to be discarded, that is not in policy stack. Discarding first policy")
        policies = policies[1:]
        return Policy.FASCIST if target == Policy.LIBERAL else Policy.LIBERAL
                
        
    def _askForOpinions(self) -> None:
        for agent in self.agents:
            everythingSaid = self._getEverythingSaid()
            self.gameStateLogger.info(f"Asking {agent.agentName} for input")
            message = agent.action(AgentAction.THINK_AND_ANSWERE, {PromptMessages.RECENT_MESSAGES: f"What has been told on the table so far: {everythingSaid}"})
            self._addMessage(message=message, agentName=agent.agentName)
            self.protocol.append(f"{agent.agentName}: {message}")

    def _voteForPresident(self) -> bool:
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
        message = f"Result of Voting for {self.presidentCandidate.agentName}: Yes: {yes}, No: {no}"
        self._addMessage(message=message)
        self.protocol.append(message)
        return yes > no
                                         
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
        self.chancellorCandidate = self._getAgent(self.chancellorCandidateName)
        message = f"{self.presidentCandidate.agentName} is the president candidate, they have choosen {self.chancellorCandidateName} as their channcellor candidate"
        self._addMessage(message=message)
        self.protocol.append(message)

    def _getChancellorCandidates(self) -> None:
        return [agent.agentName for agent in self.agents if agent.agentName != self.presidentCandidate.agentName]

    def _getAgent(self, agentName) -> BaseAgent:
        for agent in self.agents:
            if agent.agentName.strip().lower() == agentName.strip().lower():
                return agent
        self.gameStateLogger.warn(f"Chancellor {agentName} not found. Set first Player as chancellor")
        return self.agents[0]

    def _getEverythingSaid(self) -> str:
        lastMessages = self.protocol.copy() if len(self.protocol) < self.numberOfPassedMessages else self.protocol[-5:].copy()
        return ",".join(f"[{answere}]" for answere in lastMessages)

    def _logProtocol(self) -> None:
        for agent in self.agents:
            agent.logProtocol()
        if (self.protocolLogger):
            self.protocolLogger.writeLine("Result")
            for entry in self.protocol:
                self.protocolLogger.writeLine(entry)
                self.protocolLogger.writeLine("---")
            self.protocolLogger.writeLine(f"Fascist Cards played: {self.gameState.badPoliciesPlayed}, Liberal cards played: {self.gameState.goodPoliciesPlayed}")

