from move_verifier import MoveVerifier
from position import Position
from move import Move
from castling_move import CastlingMove
from vector import Vector


class MoveVerifierTestSuite():
    def getTests():
        Suite = MoveVerifierTestSuite
        return [
            {"runnable": Suite.e4, "name": "Just. 1. e4."},
            {"runnable": Suite.e4e5, "name": "Just. 1. e4 e5"},
            {"runnable": Suite.bong, "name": "JUST DOUBLE BONGCLOUD (Carleson vs Nakamura 2021)"},
            {"runnable": Suite.rchecks, "name": "King Check Checks : Rook Moves"},
            {"runnable": Suite.bchecks, "name": "King Check Checks : Bishop Moves"},
            {"runnable": Suite.nchecks, "name": "King Check Checks : Knight Moves"},
            {"runnable": Suite.qchecks, "name": "King Check Checks : Queen Moves"},
            {"runnable": Suite.pchecks, "name": "King Check Checks : Pawn Moves"},
            {"runnable": Suite.kingsindian, "name": "Just a Kings Indian Attack"},
            {"runnable": Suite.ksniper, "name": "Kingside Sniper"},
            {"runnable": Suite.qsniper, "name": "Queenside Sniper"},
            {"runnable": Suite.bdgbvqc, "name": "Just a Blackmar-Diemer Gambit Bogoljubov Variation Queenside Castling"},
        ]

    def verifyGame(position, moveList):
        res = MoveVerifier.verifyGame(position, moveList)
        if res.isLegal: 
            return res
        else:
            print(res.reason)
            return False

    def verifyIllegal(position, moveList):
        res = MoveVerifier.verifyGame(position, moveList)
        if not res.isLegal and "is being checked" in res.reason: 
            return True
        elif res.isLegal:
            print("Should be declared Illegal, but is not: \n %s" 
                % (moveList))
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

    def e4():
        return all([MoveVerifierTestSuite.verifyGame(Position.fromStartingPosition(), [
            Move.fromAN("e4")
        ])])

    def e4e5():
        return all([MoveVerifierTestSuite.verifyGame(Position.fromStartingPosition(), [
            Move.fromAN("e4"),
            Move.fromAN("e5"),
        ])])

    def bong():
        return all([MoveVerifierTestSuite.verifyGame(Position.fromStartingPosition(), [
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
        ])])

    def rchecks():
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

    def bchecks():
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

    def nchecks():
        whiteKingsJail = Position.fromFEN("8/3n2k1/1n3n2/8/n2K2n1/8/1n3n2/3n4 w - - 0 1")
        blackKingsJail = Position.fromFEN("8/3N2K1/1N3N2/8/N2k2N1/8/1N3N2/3N4 b - - 0 1")
        return all([
            MoveVerifierTestSuite.kingIsStuck(whiteKingsJail),
            MoveVerifierTestSuite.kingIsStuck(blackKingsJail)
        ])

    def qchecks():
        whiteKingsJail = Position.fromFEN("8/6k1/8/5q2/3K4/8/8/2q5 w - - 0 1")
        blackKingsJail = Position.fromFEN("8/6K1/8/5Q2/3k4/8/8/2Q5 b - - 0 1")
        return all([
            MoveVerifierTestSuite.kingIsStuck(whiteKingsJail),
            MoveVerifierTestSuite.kingIsStuck(blackKingsJail)
        ])

    def pchecks():
        whiteKingsJail = Position.fromFEN("8/6k1/2ppp3/1p3p2/1p1K1p2/8/5n2/8 w - - 0 1")
        blackKingsJail = Position.fromFEN("8/6K1/5N2/8/1P1k1P2/1P3P2/2PPP3/8 b - - 0 1")
        return all([
            MoveVerifierTestSuite.kingIsStuck(whiteKingsJail),
            MoveVerifierTestSuite.kingIsStuck(blackKingsJail)
        ])

    def kingsindian():
        kingsIndianAttack = Position.fromFEN("r1bqkbnr/pp1npppp/2p5/3p4/8/5NP1/PPPPPPBP/RNBQK2R w KQkq - 2 4")
        newPos = MoveVerifierTestSuite.verifyGame(
            kingsIndianAttack, 
            [CastlingMove.fromAN("O-O")]
        ).updatedPosition
        assert(newPos.pieceTypeIs(Vector.fromAN("f1"), "R"))
        assert(newPos.pieceTypeIs(Vector.fromAN("g1"), "K"))
        assert(newPos.pieceTypeIs(Vector.fromAN("h1"), "-"))
        return True

    def ksniper():
        kingSideSniper = Position.fromFEN("1k6/ppp5/3q4/8/8/8/PPPPP1PP/4K2R w - - 0 1")
        return all([
            MoveVerifierTestSuite.verifyGame(kingSideSniper, [
                CastlingMove.fromAN("O-O"),
                Move.fromAN("Qf8"),
                Move.fromAN("Rxf8#")
            ])
        ])

    def qsniper():
        queenSideSniper = Position.fromFEN("1k6/ppp5/5q2/8/8/8/PPP1PPPP/R3K3 w - - 0 1")
        return all([
            MoveVerifierTestSuite.verifyGame(queenSideSniper, [
                CastlingMove.fromAN("O-O-O"),
                Move.fromAN("Qd8"),
                Move.fromAN("Rxd8#")
            ])
        ])
        
    def bdgbvqc():
        BDGambit_Bogoljubov = Position.fromFEN(
            "rnbq1rk1/ppp1ppbp/5np1/8/3P1B2/2N2N2/PPPQ2PP/R3KB1R w KQ - 4 8"
        )
        newPos = MoveVerifierTestSuite.verifyGame(
            BDGambit_Bogoljubov, 
            [CastlingMove.fromAN("O-O-O")]
        ).updatedPosition
        assert(newPos.pieceTypeIs(Vector.fromAN("a1"), "-"))
        assert(newPos.pieceTypeIs(Vector.fromAN("b1"), "-"))
        assert(newPos.pieceTypeIs(Vector.fromAN("c1"), "K"))
        assert(newPos.pieceTypeIs(Vector.fromAN("d1"), "R"))
        assert(newPos.pieceTypeIs(Vector.fromAN("e1"), "-"))
        assert(newPos.pieceTypeIs(Vector.fromAN("f1"), "B"))
        assert(newPos.pieceTypeIs(Vector.fromAN("g1"), "-"))
        assert(newPos.pieceTypeIs(Vector.fromAN("h1"), "R"))
        return True