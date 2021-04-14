from move_verifier import MoveVerifier
from position import Position
from move import Move
class MoveVerifierTestSuite():
    def getTests():
        return [
            {"runnable": MoveVerifierTestSuite.test1, "name": "Just. 1. e4."},
            {"runnable": MoveVerifierTestSuite.test2, "name": "Just. 1. e4 e5"},
            {"runnable": MoveVerifierTestSuite.test3, "name": "JUST DOUBLE BONGCLOUD (Carleson vs Nakamura 2021)"},
            {"runnable": MoveVerifierTestSuite.test4, "name": "King Check Checks : Rook Moves"}#
            #{"runnable": MoveVerifierTestSuite.test4, "name": "King Check Checks : Bishop Moves"}
            #{"runnable": MoveVerifierTestSuite.test4, "name": "King Check Checks : Knight Moves"}
            #{"runnable": MoveVerifierTestSuite.test4, "name": "King Check Checks : Queen Moves"}
            #{"runnable": MoveVerifierTestSuite.test4, "name": "King Check Checks : Pawn Moves"}
        ]
    def verifyGame(position, moveList):
        res = MoveVerifier.verifyGame(position, moveList)
        if res.isLegal: 
            return True
        else:
            print(res.reason)
            return False
    def verifyIllegal(position, moveList):
        res = MoveVerifier.verifyGame(position, moveList)
        if not res.isLegal: 
            return True
        else:
            print("Should be decalred Illegal, but is not: %s %s" (position, moveList))
            return False
    def test1():
        return MoveVerifierTestSuite.verifyGame(Position.fromStartingPosition(), [
            Move.fromAN("e4")
        ])
    def test2():
        return MoveVerifierTestSuite.verifyGame(Position.fromStartingPosition(), [
            Move.fromAN("e4"),
            Move.fromAN("e5"),
        ])
    def test3():
        return MoveVerifierTestSuite.verifyGame(Position.fromStartingPosition(), [
            Move.fromAN("e4"),
            Move.fromAN("e5"),
            Move.fromAN("Ke2"),
            Move.fromAN("Ke7"),
            Move.fromAN("Ke1"),
            Move.fromAN("Ke8"),
            Move.fromAN("Ke2"),
            Move.fromAN("Ke7"),
            Move.fromAN("Ke1"),
            Move.fromAN("Ke8")
        ])
    def test4():
        whiteKingsJail = Position.fromFEN("8/6k1/2r5/5r2/3K4/1r6/4r3/8 w - - 0 1")
        blackKingsJail = Position.fromFEN("8/6K1/2R5/5R2/3k4/1R6/4R3/8 b - - 0 1")
        whiteKingsParade = Position.fromFEN("8/2r3k1/2R5/5Rr1/3K4/rR6/4R3/4r3 w - - 0 1")
        blackKingsParade = Position.fromFEN("8/2R3K1/2r5/5rR1/3k4/Rr6/4r3/4R3 b - - 0 1")
        return all([
            MoveVerifierTestSuite.verifyIllegal(whiteKingsJail, [Move.fromAN("Kc5")]),
            MoveVerifierTestSuite.verifyIllegal(whiteKingsJail, [Move.fromAN("Kd5")]),
            MoveVerifierTestSuite.verifyIllegal(whiteKingsJail, [Move.fromAN("Ke5")]),
            MoveVerifierTestSuite.verifyIllegal(whiteKingsJail, [Move.fromAN("Kc4")]),
            MoveVerifierTestSuite.verifyIllegal(whiteKingsJail, [Move.fromAN("Ke4")]),
            MoveVerifierTestSuite.verifyIllegal(whiteKingsJail, [Move.fromAN("Kc3")]),
            MoveVerifierTestSuite.verifyIllegal(whiteKingsJail, [Move.fromAN("Kd3")]),
            MoveVerifierTestSuite.verifyIllegal(whiteKingsJail, [Move.fromAN("Ke3")]),
            
            MoveVerifierTestSuite.verifyIllegal(blackKingsJail, [Move.fromAN("Kc5")]),
            MoveVerifierTestSuite.verifyIllegal(blackKingsJail, [Move.fromAN("Kd5")]),
            MoveVerifierTestSuite.verifyIllegal(blackKingsJail, [Move.fromAN("Ke5")]),
            MoveVerifierTestSuite.verifyIllegal(blackKingsJail, [Move.fromAN("Kc4")]),
            MoveVerifierTestSuite.verifyIllegal(blackKingsJail, [Move.fromAN("Ke4")]),
            MoveVerifierTestSuite.verifyIllegal(blackKingsJail, [Move.fromAN("Kc3")]),
            MoveVerifierTestSuite.verifyIllegal(blackKingsJail, [Move.fromAN("Kd3")]),
            MoveVerifierTestSuite.verifyIllegal(blackKingsJail, [Move.fromAN("Ke3")]),
            
            MoveVerifierTestSuite.verifyGame(whiteKingsParade, [Move.fromAN("Kc5")]),
            MoveVerifierTestSuite.verifyGame(whiteKingsParade, [Move.fromAN("Kd5")]),
            MoveVerifierTestSuite.verifyGame(whiteKingsParade, [Move.fromAN("Ke5")]),
            MoveVerifierTestSuite.verifyGame(whiteKingsParade, [Move.fromAN("Kc4")]),
            MoveVerifierTestSuite.verifyGame(whiteKingsParade, [Move.fromAN("Ke4")]),
            MoveVerifierTestSuite.verifyGame(whiteKingsParade, [Move.fromAN("Kc3")]),
            MoveVerifierTestSuite.verifyGame(whiteKingsParade, [Move.fromAN("Kd3")]),
            MoveVerifierTestSuite.verifyGame(whiteKingsParade, [Move.fromAN("Ke3")]),
            
            MoveVerifierTestSuite.verifyGame(blackKingsParade, [Move.fromAN("Kc5")]),
            MoveVerifierTestSuite.verifyGame(blackKingsParade, [Move.fromAN("Kd5")]),
            MoveVerifierTestSuite.verifyGame(blackKingsParade, [Move.fromAN("Ke5")]),
            MoveVerifierTestSuite.verifyGame(blackKingsParade, [Move.fromAN("Kc4")]),
            MoveVerifierTestSuite.verifyGame(blackKingsParade, [Move.fromAN("Ke4")]),
            MoveVerifierTestSuite.verifyGame(blackKingsParade, [Move.fromAN("Kc3")]),
            MoveVerifierTestSuite.verifyGame(blackKingsParade, [Move.fromAN("Kd3")]),
            MoveVerifierTestSuite.verifyGame(blackKingsParade, [Move.fromAN("Ke3")])            
        ]) 