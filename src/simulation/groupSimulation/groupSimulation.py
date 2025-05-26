from config.groupSimulationConfig.groupSimulationManager import GroupSimulationManager
from config.simulationConfig.simulationManager import SimulationManager
from data.dataManagers.realization.txtManager import TxtManager
from src.simulation.baseSimulation import BaseSimulation
from src.utils.dataObjects.simulationInstructionData import SimulationInstructionData


class GroupSimulation():

    def __init__(self, groupSimulationManager: GroupSimulationManager) -> None:
        self.groupSimulationManager = groupSimulationManager
    
    def run(self) -> None:
        itterations = 0
        targetItterations = self.groupSimulationManager.getItterations()
        while itterations < targetItterations or targetItterations == -1:
            itterations += 1
            for simulationInstructionData in self.groupSimulationManager.getSimulationInstructionData():
                self._runSimulationInstruction(simulationInstructionData)

    def _runSimulationInstruction(self, simulationInstructionData: SimulationInstructionData) -> None:
        for _ in range(simulationInstructionData.simulationItterations):
            simulationManager = SimulationManager(simulationInstructionData.simulationConfigFile)
            simulationLogger = TxtManager(filename=simulationInstructionData.protocol, folderpath=simulationInstructionData.folderpath)
            baseSimulation = BaseSimulation(simulationManager, simulationLogger)
            baseSimulation.run()