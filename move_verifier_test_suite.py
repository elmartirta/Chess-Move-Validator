from verifier.notation_parser import NotationParser
from verifier.move_verifier import MoveVerifier
from verifier.vector import Vector


class MoveVerifierTestSuite():
    @staticmethod
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

    @staticmethod
    def verifyGame(position, moveList):
        res = MoveVerifier.verifyGame(position, moveList)
        if res.isLegal: 
            return res
        else:
            print(res.reason)
            return False

    @staticmethod
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

    @staticmethod
    def kingCanMove(position):
        return all([
            MoveVerifierTestSuite.verifyGame(position, [NotationParser.parseAlgebreicNotation("Kc5")]),
            MoveVerifierTestSuite.verifyGame(position, [NotationParser.parseAlgebreicNotation("Kd5")]),
            MoveVerifierTestSuite.verifyGame(position, [NotationParser.parseAlgebreicNotation("Ke5")]),
            MoveVerifierTestSuite.verifyGame(position, [NotationParser.parseAlgebreicNotation("Kc4")]),
            MoveVerifierTestSuite.verifyGame(position, [NotationParser.parseAlgebreicNotation("Ke4")]),
            MoveVerifierTestSuite.verifyGame(position, [NotationParser.parseAlgebreicNotation("Kc3")]),
            MoveVerifierTestSuite.verifyGame(position, [NotationParser.parseAlgebreicNotation("Kd3")]),
            MoveVerifierTestSuite.verifyGame(position, [NotationParser.parseAlgebreicNotation("Ke3")]),
            
            MoveVerifierTestSuite.verifyGame(position, [NotationParser.parseAlgebreicNotation("Kc5")]),
            MoveVerifierTestSuite.verifyGame(position, [NotationParser.parseAlgebreicNotation("Kd5")]),
            MoveVerifierTestSuite.verifyGame(position, [NotationParser.parseAlgebreicNotation("Ke5")]),
            MoveVerifierTestSuite.verifyGame(position, [NotationParser.parseAlgebreicNotation("Kc4")]),
            MoveVerifierTestSuite.verifyGame(position, [NotationParser.parseAlgebreicNotation("Ke4")]),
            MoveVerifierTestSuite.verifyGame(position, [NotationParser.parseAlgebreicNotation("Kc3")]),
            MoveVerifierTestSuite.verifyGame(position, [NotationParser.parseAlgebreicNotation("Kd3")]),
            MoveVerifierTestSuite.verifyGame(position, [NotationParser.parseAlgebreicNotation("Ke3")])
        ])

    @staticmethod
    def kingIsStuck(position):
        return all([
            MoveVerifierTestSuite.verifyIllegal(position, [NotationParser.parseAlgebreicNotation("Kc5")]),
            MoveVerifierTestSuite.verifyIllegal(position, [NotationParser.parseAlgebreicNotation("Kd5")]),
            MoveVerifierTestSuite.verifyIllegal(position, [NotationParser.parseAlgebreicNotation("Ke5")]),
            MoveVerifierTestSuite.verifyIllegal(position, [NotationParser.parseAlgebreicNotation("Kc4")]),
            MoveVerifierTestSuite.verifyIllegal(position, [NotationParser.parseAlgebreicNotation("Ke4")]),
            MoveVerifierTestSuite.verifyIllegal(position, [NotationParser.parseAlgebreicNotation("Kc3")]),
            MoveVerifierTestSuite.verifyIllegal(position, [NotationParser.parseAlgebreicNotation("Kd3")]),
            MoveVerifierTestSuite.verifyIllegal(position, [NotationParser.parseAlgebreicNotation("Ke3")]),
            
            MoveVerifierTestSuite.verifyIllegal(position, [NotationParser.parseAlgebreicNotation("Kc5")]),
            MoveVerifierTestSuite.verifyIllegal(position, [NotationParser.parseAlgebreicNotation("Kd5")]),
            MoveVerifierTestSuite.verifyIllegal(position, [NotationParser.parseAlgebreicNotation("Ke5")]),
            MoveVerifierTestSuite.verifyIllegal(position, [NotationParser.parseAlgebreicNotation("Kc4")]),
            MoveVerifierTestSuite.verifyIllegal(position, [NotationParser.parseAlgebreicNotation("Ke4")]),
            MoveVerifierTestSuite.verifyIllegal(position, [NotationParser.parseAlgebreicNotation("Kc3")]),
            MoveVerifierTestSuite.verifyIllegal(position, [NotationParser.parseAlgebreicNotation("Kd3")]),
            MoveVerifierTestSuite.verifyIllegal(position, [NotationParser.parseAlgebreicNotation("Ke3")])
        ])

    @staticmethod
    def e4():
        return all([MoveVerifierTestSuite.verifyGame(NotationParser.fromStartingPosition(), [
            NotationParser.parseAlgebreicNotation("e4")
        ])])

    @staticmethod
    def e4e5():
        return all([MoveVerifierTestSuite.verifyGame(NotationParser.fromStartingPosition(), [
            NotationParser.parseAlgebreicNotation("e4"),
            NotationParser.parseAlgebreicNotation("e5"),
        ])])

    @staticmethod
    def bong():
        return all([MoveVerifierTestSuite.verifyGame(NotationParser.fromStartingPosition(), [
            NotationParser.parseAlgebreicNotation("e4"),
            NotationParser.parseAlgebreicNotation("e5"),
            NotationParser.parseAlgebreicNotation("Ke2"),
            NotationParser.parseAlgebreicNotation("Ke7"),
            NotationParser.parseAlgebreicNotation("Ke1"),
            NotationParser.parseAlgebreicNotation("Ke8"),
            NotationParser.parseAlgebreicNotation("Ke2"),
            NotationParser.parseAlgebreicNotation("Ke7"),
            NotationParser.parseAlgebreicNotation("Ke1"),
            NotationParser.parseAlgebreicNotation("Ke8")
        ])])

    @staticmethod
    def rchecks():
        whiteKingsJail = NotationParser.parsePosition("8/6k1/2r5/5r2/3K4/1r6/4r3/8 w - - 0 1")
        blackKingsJail = NotationParser.parsePosition("8/6K1/2R5/5R2/3k4/1R6/4R3/8 b - - 0 1")
        whiteKingsParade = NotationParser.parsePosition("8/2r3k1/2R5/5Rr1/3K4/rR6/4R3/4r3 w - - 0 1")
        blackKingsParade = NotationParser.parsePosition("8/2R3K1/2r5/5rR1/3k4/Rr6/4r3/4R3 b - - 0 1")
        return all([
            MoveVerifierTestSuite.kingIsStuck(whiteKingsJail),
            MoveVerifierTestSuite.kingIsStuck(blackKingsJail), 
            MoveVerifierTestSuite.kingCanMove(whiteKingsParade), 
            MoveVerifierTestSuite.kingCanMove(blackKingsParade)
        ])

    @staticmethod
    def bchecks():
        whiteKingsJail = NotationParser.parsePosition("8/6k1/2b5/8/1b1K1b2/8/4b3/8 w - - 0 1")
        blackKingsJail = NotationParser.parsePosition("8/8/2B3K1/8/1B1k1B2/8/4B3/8 b - - 0 1")
        whiteKingsParade = NotationParser.parsePosition("8/1b4k1/2P5/b5b1/1R1K1N2/b5b1/4Q3/5b2 w - - 0 1")
        blackKingsParade = NotationParser.parsePosition("8/1B4K1/2p5/B5B1/1r1k1n2/B5B1/4q3/5B2 b - - 0 1")
        return all([
            MoveVerifierTestSuite.kingIsStuck(whiteKingsJail),
            MoveVerifierTestSuite.kingIsStuck(blackKingsJail), 
            MoveVerifierTestSuite.kingCanMove(whiteKingsParade), 
            MoveVerifierTestSuite.kingCanMove(blackKingsParade)
        ])

    @staticmethod
    def nchecks():
        whiteKingsJail = NotationParser.parsePosition("8/3n2k1/1n3n2/8/n2K2n1/8/1n3n2/3n4 w - - 0 1")
        blackKingsJail = NotationParser.parsePosition("8/3N2K1/1N3N2/8/N2k2N1/8/1N3N2/3N4 b - - 0 1")
        return all([
            MoveVerifierTestSuite.kingIsStuck(whiteKingsJail),
            MoveVerifierTestSuite.kingIsStuck(blackKingsJail)
        ])

    @staticmethod
    def qchecks():
        whiteKingsJail = NotationParser.parsePosition("8/6k1/8/5q2/3K4/8/8/2q5 w - - 0 1")
        blackKingsJail = NotationParser.parsePosition("8/6K1/8/5Q2/3k4/8/8/2Q5 b - - 0 1")
        return all([
            MoveVerifierTestSuite.kingIsStuck(whiteKingsJail),
            MoveVerifierTestSuite.kingIsStuck(blackKingsJail)
        ])

    @staticmethod
    def pchecks():
        whiteKingsJail = NotationParser.parsePosition("8/6k1/2ppp3/1p3p2/1p1K1p2/8/5n2/8 w - - 0 1")
        blackKingsJail = NotationParser.parsePosition("8/6K1/5N2/8/1P1k1P2/1P3P2/2PPP3/8 b - - 0 1")
        return all([
            MoveVerifierTestSuite.kingIsStuck(whiteKingsJail),
            MoveVerifierTestSuite.kingIsStuck(blackKingsJail)
        ])

    @staticmethod
    def kingsindian():
        kingsIndianAttack = NotationParser.parsePosition("r1bqkbnr/pp1npppp/2p5/3p4/8/5NP1/PPPPPPBP/RNBQK2R w KQkq - 2 4")
        newPos = MoveVerifierTestSuite.verifyGame(
            kingsIndianAttack, 
            [NotationParser.parseAlgebreicNotation("O-O")]
        ).updatedPosition
        assert(newPos.board.pieceTypeIs(Vector.fromAN("f1"), "R")), newPos.board.printBoard()
        assert(newPos.board.pieceTypeIs(Vector.fromAN("g1"), "K")), newPos.board.printBoard()
        assert(newPos.board.pieceTypeIs(Vector.fromAN("h1"), "-")), newPos.board.printBoard()
        return True

    @staticmethod
    def ksniper():
        kingSideSniper = NotationParser.parsePosition("1k6/ppp5/3q4/8/8/8/PPPPP1PP/4K2R w - - 0 1")
        return all([
            MoveVerifierTestSuite.verifyGame(kingSideSniper, [
                NotationParser.parseAlgebreicNotation("O-O"),
                NotationParser.parseAlgebreicNotation("Qf8"),
                NotationParser.parseAlgebreicNotation("Rxf8#")
            ])
        ])

    @staticmethod
    def qsniper():
        queenSideSniper = NotationParser.parsePosition("1k6/ppp5/5q2/8/8/8/PPP1PPPP/R3K3 w - - 0 1")
        return all([
            MoveVerifierTestSuite.verifyGame(queenSideSniper, [
                NotationParser.parseAlgebreicNotation("O-O-O"),
                NotationParser.parseAlgebreicNotation("Qd8"),
                NotationParser.parseAlgebreicNotation("Rxd8#")
            ])
        ])
        
    @staticmethod
    def bdgbvqc():
        BDGambit_Bogoljubov = NotationParser.parsePosition(
            "rnbq1rk1/ppp1ppbp/5np1/8/3P1B2/2N2N2/PPPQ2PP/R3KB1R w KQ - 4 8"
        )
        newPos = MoveVerifierTestSuite.verifyGame(
            BDGambit_Bogoljubov, 
            [NotationParser.parseAlgebreicNotation("O-O-O")]
        ).updatedPosition
        assert(newPos.board.pieceTypeIs(Vector.fromAN("a1"), "-"))
        assert(newPos.board.pieceTypeIs(Vector.fromAN("b1"), "-"))
        assert(newPos.board.pieceTypeIs(Vector.fromAN("c1"), "K"))
        assert(newPos.board.pieceTypeIs(Vector.fromAN("d1"), "R"))
        assert(newPos.board.pieceTypeIs(Vector.fromAN("e1"), "-"))
        assert(newPos.board.pieceTypeIs(Vector.fromAN("f1"), "B"))
        assert(newPos.board.pieceTypeIs(Vector.fromAN("g1"), "-"))
        assert(newPos.board.pieceTypeIs(Vector.fromAN("h1"), "R"))
        return True