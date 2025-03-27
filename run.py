from config.simulationConfig.simulationManager import SimulationManager
from data.dataManagers.realization.txtManager import TxtManager

from src.simulation.baseSimulation import BaseSimulation

def main():
    simulationManager = SimulationManager("table_discussion")
    simulationLogger = TxtManager(filename="SimulationProtocol", folderpath="discussions")
    baseSimulation = BaseSimulation(simulationManager, simulationLogger)
    baseSimulation.run()

if __name__ == "__main__":
    main()