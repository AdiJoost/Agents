from pathlib import Path
from config.rootPath import getRootPath
from data.dataManagers.abstracts.fileManager import FileManager
from log.logger import Logger


class PromptManager():

    FILE_TYPE: str = "txt"

    def __init__(self, folderpath: str="data/prompts") -> None:
        self._absolutPath = self._getAbsolutePath(folderpath)
        self.logger = Logger(loggerName="TxtManager")

    def _getPrompt(self, fileName) -> str:
        filepath = self._absolutPath.joinpath(f"{fileName}.{self.FILE_TYPE}")
        with open(filepath, "r", encoding="UTF-8") as file:
            return file.read()
        
    def getPrompt(self, fileName: str, argsToReplace: dict= None) -> str:
        '''Reads the file and replaces the keys in argsToReplace with their values'''
        prompt: str = self._getPrompt(fileName)
        if argsToReplace:
            for key, value in argsToReplace.items():
                prompt.replace(key, value)
        return prompt
        
    def _getAbsolutePath(self, folderPath: str) -> Path:
        rootPath = getRootPath()
        return rootPath.joinpath(folderPath)
