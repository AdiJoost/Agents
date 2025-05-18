

import json
from pathlib import Path
from typing import List

from config.groupSimulationConfig.groupSimulationConfigFields import GroupSimulationConfigFields
from config.rootPath import getRootPath
from config.simulationConfig.simulationConfigFields import SimulationConfigFields
from data.dataManagers.realization.promptManager import PromptManager
from src.agents.baseAgent import BaseAgent
from src.utils.dataObjects.simulationInstructionData import SimulationInstructionData



class GroupSimulationManager():

    def __init__(self, fileName: str) -> None:
        self.fileName = fileName
        self.filePath = self._getFilePath()
        self.values = self._loadConfig()

    def getNumberOfFacists(self) -> int:
        return self.values.get(SimulationConfigFields.NUMBER_OF_FASCISTS, 0)

    def getSimulationInstructionData(self, promptManager: PromptManager) -> List[SimulationInstructionData]:
        returnValue = []
        simulations = self.values.get(GroupSimulationConfigFields.SIMULATIONS)
        if not simulations:
            return returnValue
        for simulation in simulations:
            returnValue.append(SimulationInstructionData(**simulation))
        return returnValue  
    
    def getItterations(self) -> int:
        return self.values.get(GroupSimulationConfigFields.ITTERATIONS, -1)

    def getFileName(self) -> str:
        return self.fileName

    def _getFilePath(self) -> Path:
        rootPath = getRootPath()
        return rootPath.joinpath("config", "groupSimulationConfig", f"{self.fileName}.json")
    
    def _loadConfig(self) -> dict:
        with open(self.filePath, "r") as file:
            return json.load(file)