from verifier.notation_parser import NotationParser
from verifier.game import Game, UnfinishedGame


class GameTestSuite():
    @classmethod
    def getTests(cls):
        return [
            {"runnable": cls.canInitializeGame, "name": "Can initialize a Game object"},
            {"runnable": cls.canInitializeUnfinishedGame, "name": "Can initialize an Unfinished Game object"},
            {"runnable": cls.canAppendMoves, "name": "Can append moves to the Game object"}
        ]
    
    @staticmethod
    def canInitializeGame():
        game = Game()
        return True
    
    @staticmethod
    def canInitializeUnfinishedGame():
        game = UnfinishedGame()
        return True

    @staticmethod
    def canAppendMoves():
        game = UnfinishedGame()
        game.append(NotationParser.parseAlgebreicNotation("e4"))
        game.append(NotationParser.parseAlgebreicNotation("O-O"))
        return True