class SimulationInstructionData():

    def __init__(self, simulationConfigFile: str, protocol: str, folderpath: str, simulationItterations: int) -> None:
        self.simulationConfigFile = simulationConfigFile
        self.protocol = protocol
        self.folderpath = folderpath
        self.simulationItterations = simulationItterations