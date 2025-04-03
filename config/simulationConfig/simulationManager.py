

import json
from pathlib import Path
from typing import List

from config.rootPath import getRootPath
from config.simulationConfig.simulationConfigFields import SimulationConfigFields
from src.agents.baseAgent import BaseAgent



class SimulationManager():

    def __init__(self, fileName: str) -> None:
        self.fileName = fileName
        self.filePath = self._getFilePath()
        self.values = self._loadConfig()

    def getNumberOfFacists(self) -> int:
        return self.values.get(SimulationConfigFields.NUMBER_OF_FASCISTS, 0)

    def getAgents(self) -> List[BaseAgent]:
        returnValue = []
        agents = self.values.get(SimulationConfigFields.AGENTS)
        if not agents:
            return returnValue
        for agent in agents:
            returnValue.append(self._getAgent(agent))
        return returnValue  
    
    def getInitialPrompt(self) -> str:
        return self.values.get(SimulationConfigFields.INITIAL_PROMPT, "")
        
    def getQuestion(self) -> str:
        return self.values.get(SimulationConfigFields.QUESTION, "")

    def getFileName(self) -> str:
        return self.fileName

    def _getFilePath(self) -> Path:
        rootPath = getRootPath()
        return rootPath.joinpath("config", "simulationConfig", f"{self.fileName}.json")
    
    def _loadConfig(self) -> dict:
        with open(self.filePath, "r") as file:
            return json.load(file)
        
    def _getAgent(self, agentValues: dict) -> BaseAgent:
        agentInstructions = self._getAgentInstruction(agentValues)
        agentName = agentValues.get(SimulationConfigFields.AGENT_NAME, "Unnamed")
        agentRole = agentValues.get(SimulationConfigFields.AGENT_ROLE, "No Role")
        agentRoleDescription = agentValues.get(SimulationConfigFields.AGENT_ROLE_DESCRIPTION, "")
        model = agentValues.get(SimulationConfigFields.MODEL)
        return BaseAgent(agentName=agentName, agentRole=agentRole, agentRoleDescription=agentRoleDescription, agentInstructions=agentInstructions, model=model)
    
    def _getAgentInstruction(self, agentValues: dict) -> str:
        generalModelInstructions = self.values.get(SimulationConfigFields.GENERAL_MODEL_INSTRUCTIONS, "")
        agentName = agentValues.get(SimulationConfigFields.AGENT_NAME, "Unnamed")
        agentRole = agentValues.get(SimulationConfigFields.AGENT_ROLE, "No Role")
        agentRoleDescription = agentValues.get(SimulationConfigFields.AGENT_ROLE_DESCRIPTION, "")
        return f"Generel Instructions for you: {generalModelInstructions} You're named: {agentName} Your Role is: {agentRole}, Your Role description is: {agentRoleDescription}"
    
