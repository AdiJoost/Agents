import os
from config.applicationConfig.applicationConfigFields import ApplicationConfigFields
from config.configManager import getConfig
from config.simulationConfig.simulationManager import SimulationManager
from data.dataManagers.realization.txtManager import TxtManager

from src.facade.api.app import app
from src.simulation.baseSimulation import BaseSimulation
from src.utils.serverConfig.serverConfig import ServerConfig

def main():
    simulationManager = SimulationManager("6playersNoReason")
    #simulationManager = SimulationManager("table_discussion")
    simulationLogger = TxtManager(filename="SimulationProtocol", folderpath="discussions")
    baseSimulation = BaseSimulation(simulationManager, simulationLogger)
    baseSimulation.run()

def startAPI():
    port = getConfig(name=ApplicationConfigFields.PORT.value)
    app.run(host="0.0.0.0" ,port=port, debug=True)

def test():
    print(ServerConfig.getMongoAddress())
    print(ServerConfig.getOllamaAddress())

if __name__ == "__main__":
    startAPI() 
       