from config.applicationConfig.applicationConfigFields import ApplicationConfigFields
from config.configManager import getConfig
from config.simulationConfig.simulationManager import SimulationManager
from data.dataManagers.realization.txtManager import TxtManager

from src.facade.api.app import app
from src.simulation.baseSimulation import BaseSimulation

def main():
    simulationManager = SimulationManager("table_discussion")
    simulationLogger = TxtManager(filename="SimulationProtocol", folderpath="discussions")
    baseSimulation = BaseSimulation(simulationManager, simulationLogger)
    baseSimulation.run()

def startAPI():
    port = getConfig(name=ApplicationConfigFields.PORT.value)
    app.run(host="0.0.0.0" ,port=port, debug=True)

if __name__ == "__main__":
    startAPI() 
    