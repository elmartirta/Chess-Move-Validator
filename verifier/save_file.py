from typing import List
from verifier.game import UnfinishedGame


class SaveFile():
    def __init__(self, path: str = ""):
        self.path: str = path
    
    def parse(self) -> UnfinishedGame:
        lines = self._readSelf()
        game = UnfinishedGame()
        for line in lines:
            self._parseLine(line, game)
        return game
    
    def _readSelf(self) -> List[str]:
        with open(self.path, "r") as file:
            return file.readlines()
             
    @staticmethod
    def _parseLine(line: str, game: UnfinishedGame):
        pass