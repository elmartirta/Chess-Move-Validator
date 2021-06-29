from verifier.game import Game


class GameTestSuite():
    @classmethod
    def getTests(cls):
        return [
            {"runnable": cls.canInitializeGame, "name": "Can initialize a Game object"}
        ]
    
    def canInitializeGame():
        game = Game()
        return True