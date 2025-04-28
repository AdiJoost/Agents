from data.dataManagers.abstracts.fileManager import FileManager
from log.logger import Logger


class TxtManager(FileManager):

    FILE_TYPE: str = "txt"

    def __init__(self, filename, folderpath: str,) -> None:
        super().__init__(filename, folderpath, self.FILE_TYPE)
        self.logger = Logger(loggerName="TxtManager")

    def writeLine(self, line: str) -> None:
        with open(self.absolutPath, "a", encoding="UTF-8", newline="") as file:
            file.write(line)
            file.write("\n")

    def getText(self) -> str:
        with open(self.absolutPath, "r", encoding="UTF-8") as file:
            return file.read()
