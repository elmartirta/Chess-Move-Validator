from vector import Vector
from move_generator import MoveGenerator
from castling_move import CastlingMove

class MoveGeneratorTestSuite():
    @staticmethod
    def getTests():
        return [
            {"runnable": MoveGeneratorTestSuite.moveOneA3, "name": "Generate 1.a3"},
            {"runnable": MoveGeneratorTestSuite.moveOneA4, "name": "Generate 1.a4"},
            {"runnable": MoveGeneratorTestSuite.moveOneNA4, "name": "Generate 1.Na4"},
            {"runnable": MoveGeneratorTestSuite.moveOneE4, "name": "Generate 1.e4"},
            {"runnable": MoveGeneratorTestSuite.allTob3, "name": "Generate Moves from all pieces to B3"},
            {"runnable": MoveGeneratorTestSuite.rGen, "name": "Generate lots of simple rook moves"},
            {"runnable": MoveGeneratorTestSuite.bGen, "name": "Generate lots of simple bishop moves"},
            {"runnable": MoveGeneratorTestSuite.nGen, "name": "Generate lots of simple knight moves"},
            {"runnable": MoveGeneratorTestSuite.qGen, "name": "Generate lots of simple queen moves"},
            {"runnable": MoveGeneratorTestSuite.kGen, "name": "Generate lots of simple king moves"},
            {"runnable": MoveGeneratorTestSuite.pGen, "name": "Generate lots of simple pawn moves"},
            {"runnable": MoveGeneratorTestSuite.rAmbGen, "name": "Generate ambiguous rook moves"},
            {"runnable": MoveGeneratorTestSuite.bAmbGen, "name": "Generate ambiguous bishop moves"},
            {"runnable": MoveGeneratorTestSuite.qAmbGen, "name": "Generate ambiguous queen moves"},
            {"runnable": MoveGeneratorTestSuite.castle, "name": "Generate castling moves"}
        ]
        
    @staticmethod
    def moveOneA3():
        candidateMoves = MoveGenerator.generateMoveListFromStartingPosition("a3")
        assert(len(candidateMoves) == 1), str(candidateMoves)
        assert(candidateMoves[0].pieceType == "P"), candidateMoves[0]
        assert(candidateMoves[0].source == Vector.fromAN("a2")), candidateMoves[0].source.toAN()
        assert(candidateMoves[0].destination == Vector.fromAN("a3")), candidateMoves[0].destination.toAN()
        return True
    
    @staticmethod
    def moveOneA4():
        candidateMoves = MoveGenerator.generateMoveListFromStartingPosition("a4")
        assert(len(candidateMoves) == 1), str(candidateMoves)
        assert(candidateMoves[0].pieceType == "P"), candidateMoves[0]
        assert(candidateMoves[0].source == Vector.fromAN("a2")), candidateMoves[0].source.toAN()
        assert(candidateMoves[0].destination == Vector.fromAN("a4")), candidateMoves[0].destination.toAN()
        return True
    
    @staticmethod
    def moveOneNA4():
        candidateMoves = MoveGenerator.generateMoveListFromStartingPosition("Na3")
        assert(len(candidateMoves) == 1), str(candidateMoves)
        assert(candidateMoves[0].pieceType == "N"), candidateMoves[0]
        assert(candidateMoves[0].source == Vector.fromAN("b1")), candidateMoves[0].source.toAN()
        assert(candidateMoves[0].destination == Vector.fromAN("a3")), candidateMoves[0].destination.toAN()
        return True

    @staticmethod
    def moveOneE4():
        candidateMoves = MoveGenerator.generateMoveListFromStartingPosition("e4")
        assert(len(candidateMoves) == 1), str(candidateMoves)
        assert(candidateMoves[0].pieceType == "P"), candidateMoves[0]
        assert(candidateMoves[0].source == Vector.fromAN("e2")), candidateMoves[0].source.toAN()
        assert(candidateMoves[0].destination == Vector.fromAN("e4")), candidateMoves[0].destination.toAN()
        return True

    @staticmethod
    def allTob3():
        pos = "8/1R3B2/8/6k1/8/5Q2/1PKN4/8 w - - 0 1"
        res = lambda pos, move: MoveGenerator.generateMoveListFromFEN(pos, move)
        check = lambda pos, move: res(pos,move) != None and len(res(pos,move)) != 0
        assert(check("8/1R3B2/8/6k1/8/5Q2/1PKN4/8 w - - 0 1", "Rb3"))
        assert(check(pos, "Bb3"))
        assert(check(pos, "Nb3"))
        assert(check(pos, "Qb3"))
        assert(check(pos, "Kb3"))
        assert(check(pos, "b3"))
        assert(check(pos, "b4"))
        fails = lambda pos, move: res(pos,move) != None and len(res(pos,move)) == 0
        assert(fails(pos, "Rc4"))
        assert(fails(pos, "Bb4"))
        assert(fails(pos, "Nb2"))
        assert(fails(pos, "Qb4"))
        assert(fails(pos, "Kc4"))
        assert(fails(pos, "c3"))
        assert(fails(pos, "c4"))
        return True

    @staticmethod
    def rGen():
        res = lambda pos, move: MoveGenerator.generateMoveListFromFEN(pos, move)
        check = lambda pos, move: res(pos,move) != None and len(res(pos,move)) != 0
        assert(check("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Ra2"))
        assert(check("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Rb1"))
        assert(check("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Ra8"))
        assert(check("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Rh1"))
        assert(check("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Rg1+"))
        assert(check("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Ra7+"))
        fails = lambda pos, move: res(pos,move) != None and len(res(pos,move)) == 0
        assert(fails("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Rb3"))
        assert(fails("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Rc2"))
        assert(fails("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Rb8"))
        assert(fails("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Rh2"))
        assert(fails("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Rg2+"))
        assert(fails("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Rb7+"))
        assert(fails("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Ra1"))
        return True

    @staticmethod
    def bGen():
        res = lambda pos, move: MoveGenerator.generateMoveListFromFEN(pos, move)
        check = lambda pos, move: res(pos,move) != None and len(res(pos,move)) != 0
        assert(check("8/8/2K5/8/3B4/5k2/8/8 w - - 0 1", "Ba1"))
        assert(check("8/8/2K5/8/3B4/5k2/8/8 w - - 0 1", "Bh8"))
        assert(check("8/8/2K5/8/3B4/5k2/8/8 w - - 0 1", "Ba7"))
        assert(check("8/8/2K5/8/3B4/5k2/8/8 w - - 0 1", "Bg1"))
        fails = lambda pos, move: res(pos,move) != None and len(res(pos,move)) == 0
        assert(fails("8/8/2K5/8/3B4/5k2/8/8 w - - 0 1", "Ba2"))
        assert(fails("8/8/2K5/8/3B4/5k2/8/8 w - - 0 1", "Bg8"))
        assert(fails("8/8/2K5/8/3B4/5k2/8/8 w - - 0 1", "Ba6"))
        assert(fails("8/8/2K5/8/3B4/5k2/8/8 w - - 0 1", "Bg2"))
        assert(fails("8/8/2K5/8/3B4/5k2/8/8 w - - 0 1", "Bd4"))
        return True

    @staticmethod
    def nGen():
        res = lambda pos, move: MoveGenerator.generateMoveListFromFEN(pos, move)
        check = lambda pos, move: res(pos,move) != None and len(res(pos,move)) != 0
        fourKnightsGame = "r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/2N2N2/PPPP1PPP/R1BQKB1R w KQkq - 4 4"
        assert(check(fourKnightsGame, "Nb5"))
        assert(check(fourKnightsGame, "Na4"))
        assert(check(fourKnightsGame, "Ng1"))
        assert(check(fourKnightsGame, "Ne2"))
        fails = lambda pos, move: res(pos,move) != None and len(res(pos,move)) == 0
        assert(fails(fourKnightsGame, "Nc4"))
        assert(fails(fourKnightsGame, "Nc1"))
        assert(fails(fourKnightsGame, "Nh3"))
        assert(fails(fourKnightsGame, "Nh8"))
        assert(fails(fourKnightsGame, "Nc3"))
        assert(fails(fourKnightsGame, "Nf3"))
        return True

    @staticmethod
    def qGen():
        res = lambda pos, move: MoveGenerator.generateMoveListFromFEN(pos, move)
        check = lambda pos, move: res(pos,move) != None and len(res(pos,move)) != 0
        scandanavian = "rnb1kbnr/ppp1pppp/8/3q4/8/2N5/PPPP1PPP/R1BQKBNR b KQkq - 1 3"
        assert(check(scandanavian, "Qa5"))
        assert(check(scandanavian, "Qe5+"))
        assert(check(scandanavian, "Qe6+"))
        assert(check(scandanavian, "Qxd2+"))
        assert(check(scandanavian, "Qxa2"))
        assert(check(scandanavian, "Qxg2"))
        fails = lambda pos, move: res(pos,move) != None and len(res(pos,move)) == 0
        assert(fails(scandanavian, "Qxc3"))
        assert(fails(scandanavian, "Qxf2"))
        assert(fails(scandanavian, "Qxh2"))
        assert(fails(scandanavian, "Qxh8"))
        assert(fails(scandanavian, "Qxb8"))
        assert(fails(scandanavian, "Qf6"))
        return True

    @staticmethod
    def kGen():
        res = lambda pos, move: MoveGenerator.generateMoveListFromFEN(pos, move)
        check = lambda pos, move: res(pos,move) != None and len(res(pos,move)) != 0
        assert(check("8/8/8/5K2/8/8/1k6/3r4 w - - 4 3", "Ke6"))
        assert(check("8/8/8/5K2/8/8/1k6/3r4 w - - 4 3", "Ke5"))
        assert(check("8/8/8/5K2/8/8/1k6/3r4 w - - 4 3", "Ke4"))
        assert(check("8/8/8/5K2/8/8/1k6/3r4 w - - 4 3", "Kg6"))
        assert(check("8/8/8/5K2/8/8/1k6/3r4 w - - 4 3", "Kg5"))
        assert(check("8/8/8/5K2/8/8/1k6/3r4 w - - 4 3", "Kg4"))
        assert(check("8/8/8/5K2/8/8/1k6/3r4 w - - 4 3", "Kf6"))
        assert(check("8/8/8/5K2/8/8/1k6/3r4 w - - 4 3", "Kf4"))
        fails = lambda pos, move: res(pos,move) != None and len(res(pos,move)) == 0
        assert(fails("8/8/8/5K2/8/8/1k6/3r4 w - - 4 3", "Kf5"))
        assert(fails("8/8/8/5K2/8/8/1k6/3r4 w - - 4 3", "Kh8"))
        assert(fails("8/8/8/5K2/8/8/1k6/3r4 w - - 4 3", "Ka8"))
        assert(fails("8/8/8/5K2/8/8/1k6/3r4 w - - 4 3", "Kh1"))
        return True

    @staticmethod
    def pGen():
        res = lambda pos, move: MoveGenerator.generateMoveListFromFEN(pos, move)
        check = lambda pos, move: res(pos,move) != None and len(res(pos,move)) != 0
        pos = "rnbqkbnr/p3pp1p/1p4p1/2ppP3/1P6/2P5/P2P1PPP/RNBQKBNR w KQkq d6 0 5"
        assert(check(pos, "a3"))
        assert(check(pos, "a4"))
        assert(check(pos, "b5"))
        assert(check(pos, "bxc5"))
        assert(check(pos, "c4"))
        assert(check(pos, "d3"))
        assert(check(pos, "d4"))
        assert(check(pos, "exd6"))
        assert(check(pos, "f4"))
        assert(check(pos, "g3"))
        assert(check(pos, "h4"))
        assert(check(pos, "h3"))
        fails = lambda pos, move: res(pos,move) != None and len(res(pos,move)) == 0
        assert(fails(pos, "b3"))
        assert(fails(pos, "c5"))
        assert(fails(pos, "a7"))
        assert(fails(pos, "h2"))
        assert(fails(pos, "e2"))
        assert(fails(pos, "e4"))
        assert(fails(pos, "c3"))
        assert(fails(pos, "c2"))
        return True

    @staticmethod
    def rAmbGen():
        res = lambda pos, move: MoveGenerator.generateMoveListFromFEN(pos, move)
        check2 = lambda pos, move: res(pos,move) != None and len(res(pos,move)) == 2
        check4= lambda pos, move: res(pos,move) != None and len(res(pos,move)) == 4
        assert(check2("8/8/5k2/8/R7/8/1K6/3R4 w - - 0 1", "Rd4"))
        assert(check2("8/8/5k2/8/R6R/8/1K6/8 w - - 0 1", "Rd4"))
        assert(check2("8/8/5k2/8/RR6/8/1K6/8 w - - 0 1", "Rd4"))
        assert(check2("3R4/3R4/5k2/8/8/8/1K6/8 w - - 0 1", "Rd4"))
        assert(check2("R7/8/5k2/8/8/2K5/8/7R w - - 0 1", "Ra1"))
        assert(check2("R7/8/5k2/8/8/2K5/8/7R w - - 0 1", "Rh8"))
        assert(check4("8/R7/R4k2/8/8/R1K5/R7/8 w - - 0 1", "Ra1"))
        assert(check4("8/R7/R4k2/8/8/R1K5/R7/8 w - - 0 1", "Ra4"))
        assert(check4("8/R7/R4k2/8/8/R1K5/R7/8 w - - 0 1", "Ra5"))
        assert(check4("8/R7/R4k2/8/8/R1K5/R7/8 w - - 0 1", "Ra8"))
        assert(check4("3R1R2/8/5k2/8/8/2K4R/8/7R w - - 0 1", "Rh8"))
        return True

    @staticmethod
    def bAmbGen():
        res = lambda pos, move: MoveGenerator.generateMoveListFromFEN(pos, move)
        check2 = lambda pos, move: res(pos,move) != None and len(res(pos,move)) == 2
        check4= lambda pos, move: res(pos,move) != None and len(res(pos,move)) == 4
        assert(check2("8/4k3/1B6/8/8/8/1BK5/8 w - - 0 1", "B2d4"))
        assert(check2("8/4k3/1B6/8/8/8/1BK5/8 w - - 0 1", "B2d4"))
        assert(check2("8/4k3/8/8/8/8/1BK5/6B1 w - - 0 1", "Bd4"))
        assert(check2("7B/4k3/8/8/8/8/1BK5/8 w - - 0 1", "Bd4"))
        assert(check2("8/4k3/8/8/8/8/1BK5/B7 w - - 0 1", "Bd4"))
        return True

    @staticmethod
    def qAmbGen():
        res = lambda pos, move: MoveGenerator.generateMoveListFromFEN(pos, move)
        check2 = lambda pos, move: res(pos,move) != None and len(res(pos,move)) == 2
        check4 = lambda pos, move: res(pos,move) != None and len(res(pos,move)) == 4
        assert(check2("3Q4/6k1/8/8/8/7Q/1K6/8 w - - 0 1", "Qd3"))
        assert(check2("3Q4/6k1/8/8/8/7Q/1K6/8 w - - 0 1", "Qh8"))
        assert(check2("3Q4/6k1/8/8/8/7Q/1K6/8 w - - 0 1", "Qh4"))
        assert(check2("3Q4/6k1/8/8/8/7Q/1K6/8 w - - 0 1", "Qd7"))
        assert(check4("6k1/3Q4/8/1Q6/8/7Q/1K6/5Q2 w - - 0 1", "Qd3"))
        assert(check4("6k1/3Q4/8/1Q6/8/7Q/1K6/5Q2 w - - 0 1", "Qf5"))
        return True

    @staticmethod
    def castle():
        res = lambda pos, move: MoveGenerator.generateMoveListFromFEN(pos, move)
        check = lambda pos, move: res(pos, move) != None and isinstance(res(pos, move)[0], CastlingMove)
        assert(res("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w - - 0 1", "O-O"))
        assert(res("r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w - - 0 1", "O-O-O"))
        return True