from move_verifier import MoveVerifier
from position import Position
from move import Move
class MoveVerifierTestSuite():
    def getTests():
        return [
            {"runnable": MoveVerifierTestSuite.test1, "name": "Just. 1. e4."},
            {"runnable": MoveVerifierTestSuite.test2, "name": "Just. 1. e4 e5"},
            {"runnable": MoveVerifierTestSuite.test3, "name": "JUST DOUBLE BONGCLOUD (Carleson vs Nakamura 2021)"},
            {"runnable": MoveVerifierTestSuite.test4, "name": "King Check Checks : Rook Moves"},
            {"runnable": MoveVerifierTestSuite.test5, "name": "King Check Checks : Bishop Moves"},
            {"runnable": MoveVerifierTestSuite.test6, "name": "King Check Checks : Knight Moves"},
            {"runnable": MoveVerifierTestSuite.test7, "name": "King Check Checks : Queen Moves"},
            {"runnable": MoveVerifierTestSuite.test8, "name": "King Check Checks : Pawn Moves"}
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
        if not res.isLegal and "is being checked" in res.reason: 
            return True
        elif res.isLegal:
            print("Should be declared Illegal, but is not: \n %s %s" % (position.boardState.toString(), moveList))
        else:
            print(res.reason)
            return False
    def kingCanMove(position):
        return all([
            MoveVerifierTestSuite.verifyGame(position, [Move.fromAN("Kc5")]),
            MoveVerifierTestSuite.verifyGame(position, [Move.fromAN("Kd5")]),
            MoveVerifierTestSuite.verifyGame(position, [Move.fromAN("Ke5")]),
            MoveVerifierTestSuite.verifyGame(position, [Move.fromAN("Kc4")]),
            MoveVerifierTestSuite.verifyGame(position, [Move.fromAN("Ke4")]),
            MoveVerifierTestSuite.verifyGame(position, [Move.fromAN("Kc3")]),
            MoveVerifierTestSuite.verifyGame(position, [Move.fromAN("Kd3")]),
            MoveVerifierTestSuite.verifyGame(position, [Move.fromAN("Ke3")]),
            
            MoveVerifierTestSuite.verifyGame(position, [Move.fromAN("Kc5")]),
            MoveVerifierTestSuite.verifyGame(position, [Move.fromAN("Kd5")]),
            MoveVerifierTestSuite.verifyGame(position, [Move.fromAN("Ke5")]),
            MoveVerifierTestSuite.verifyGame(position, [Move.fromAN("Kc4")]),
            MoveVerifierTestSuite.verifyGame(position, [Move.fromAN("Ke4")]),
            MoveVerifierTestSuite.verifyGame(position, [Move.fromAN("Kc3")]),
            MoveVerifierTestSuite.verifyGame(position, [Move.fromAN("Kd3")]),
            MoveVerifierTestSuite.verifyGame(position, [Move.fromAN("Ke3")])
        ])
    def kingIsStuck(position):
        return all([
            MoveVerifierTestSuite.verifyIllegal(position, [Move.fromAN("Kc5")]),
            MoveVerifierTestSuite.verifyIllegal(position, [Move.fromAN("Kd5")]),
            MoveVerifierTestSuite.verifyIllegal(position, [Move.fromAN("Ke5")]),
            MoveVerifierTestSuite.verifyIllegal(position, [Move.fromAN("Kc4")]),
            MoveVerifierTestSuite.verifyIllegal(position, [Move.fromAN("Ke4")]),
            MoveVerifierTestSuite.verifyIllegal(position, [Move.fromAN("Kc3")]),
            MoveVerifierTestSuite.verifyIllegal(position, [Move.fromAN("Kd3")]),
            MoveVerifierTestSuite.verifyIllegal(position, [Move.fromAN("Ke3")]),
            
            MoveVerifierTestSuite.verifyIllegal(position, [Move.fromAN("Kc5")]),
            MoveVerifierTestSuite.verifyIllegal(position, [Move.fromAN("Kd5")]),
            MoveVerifierTestSuite.verifyIllegal(position, [Move.fromAN("Ke5")]),
            MoveVerifierTestSuite.verifyIllegal(position, [Move.fromAN("Kc4")]),
            MoveVerifierTestSuite.verifyIllegal(position, [Move.fromAN("Ke4")]),
            MoveVerifierTestSuite.verifyIllegal(position, [Move.fromAN("Kc3")]),
            MoveVerifierTestSuite.verifyIllegal(position, [Move.fromAN("Kd3")]),
            MoveVerifierTestSuite.verifyIllegal(position, [Move.fromAN("Ke3")])
        ])
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
            MoveVerifierTestSuite.kingIsStuck(whiteKingsJail),
            MoveVerifierTestSuite.kingIsStuck(blackKingsJail), 
            MoveVerifierTestSuite.kingCanMove(whiteKingsParade), 
            MoveVerifierTestSuite.kingCanMove(blackKingsParade)
        ])
    def test5():
        whiteKingsJail = Position.fromFEN("8/6k1/2b5/8/1b1K1b2/8/4b3/8 w - - 0 1")
        blackKingsJail = Position.fromFEN("8/8/2B3K1/8/1B1k1B2/8/4B3/8 b - - 0 1")
        whiteKingsParade = Position.fromFEN("8/1b4k1/2P5/b5b1/1R1K1N2/b5b1/4Q3/5b2 w - - 0 1")
        blackKingsParade = Position.fromFEN("8/1B4K1/2p5/B5B1/1r1k1n2/B5B1/4q3/5B2 b - - 0 1")
        return all([
            MoveVerifierTestSuite.kingIsStuck(whiteKingsJail),
            MoveVerifierTestSuite.kingIsStuck(blackKingsJail), 
            MoveVerifierTestSuite.kingCanMove(whiteKingsParade), 
            MoveVerifierTestSuite.kingCanMove(blackKingsParade)
        ])
    def test6():
        whiteKingsJail = Position.fromFEN("8/3n2k1/1n3n2/8/n2K2n1/8/1n3n2/3n4 w - - 0 1")
        blackKingsJail = Position.fromFEN("8/3N2K1/1N3N2/8/N2k2N1/8/1N3N2/3N4 b - - 0 1")
        return all([
            MoveVerifierTestSuite.kingIsStuck(whiteKingsJail),
            MoveVerifierTestSuite.kingIsStuck(blackKingsJail)
        ])
    def test7():
        whiteKingsJail = Position.fromFEN("8/6k1/8/5q2/3K4/8/8/2q5 w - - 0 1")
        blackKingsJail = Position.fromFEN("8/6K1/8/5Q2/3k4/8/8/2Q5 b - - 0 1")
        return all([
            MoveVerifierTestSuite.kingIsStuck(whiteKingsJail),
            MoveVerifierTestSuite.kingIsStuck(blackKingsJail)
        ])
    def test8():
        whiteKingsJail = Position.fromFEN("8/6k1/2ppp3/1p3p2/1p1K1p2/8/5n2/8 w - - 0 1")
        blackKingsJail = Position.fromFEN("8/6K1/5N2/8/1P1k1P2/1P3P2/2PPP3/8 b - - 0 1")
        return all([
            MoveVerifierTestSuite.kingIsStuck(whiteKingsJail),
            MoveVerifierTestSuite.kingIsStuck(blackKingsJail)
        ])