

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
    
    def getNumberOfFacistsPolicies(self) -> int:
        return self.values.get(SimulationConfigFields.NUMBER_OF_FACIST_POLICIES, 11)
    
    def getNumberOfLiberalPolicies(self) -> int:
        return self.values.get(SimulationConfigFields.NUMBER_OF_LIBERAL_POLICIES, 6)

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
        agentRoleDescription = agentValues.get(SimulationConfigFields.AGENT_ROLE_DESCRIPTION, ""),
        useReflection = agentValues.get(SimulationConfigFields.USE_REFLECTION, False)
        useReasoning = agentValues.get(SimulationConfigFields.USE_REASONING, False)
        model = agentValues.get(SimulationConfigFields.MODEL)
        return BaseAgent(agentName=agentName, agentRole=agentRole, agentRoleDescription=agentRoleDescription, agentInstructions=agentInstructions, model=model, useReasoning=useReasoning, useReflection=useReflection)
    
    def _getAgentInstruction(self, agentValues: dict) -> str:
        generalModelInstructionsObject = self.values.get(SimulationConfigFields.GENERAL_MODEL_INSTRUCTIONS, "")
        generalModelInstructions = self._getPrompt(generalModelInstructionsObject)
        agentName = agentValues.get(SimulationConfigFields.AGENT_NAME, "Unnamed")
        agentRole = agentValues.get(SimulationConfigFields.AGENT_ROLE, "No Role")
        agentRoleDescription = agentValues.get(SimulationConfigFields.AGENT_ROLE_DESCRIPTION, "")
        return f"Generel Instructions for you: {generalModelInstructions} You're named: {agentName} Your behave like: {agentRole}, Your personality is: {agentRoleDescription}"
    
    def _getPrompt(self, promptObject: dict) -> str:
        if (promptObject.get(SimulationConfigFields.PROMPT_PATH)):
            return self._loadPromptFromPath(promptObject.get(SimulationConfigFields.PROMPT_PATH))
        return promptObject.get(SimulationConfigFields.TEXT_PROMPT, "")
    
    def _loadPromptFromPath(self, path: str) -> str:
        rootPath = getRootPath()
        filePath = rootPath.joinpath(path)
        with open(filePath, "r", encoding="utf-8") as file:
            return file.read()