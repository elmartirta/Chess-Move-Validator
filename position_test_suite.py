from position import *
from move import *
from vector import Vector 
class PositionTestSuite():
    def getTests():
        return [
            {"runnable": PositionTestSuite.test1, "name": "Chess Starting Position Initialized Correctly"},
            {"runnable": PositionTestSuite.test2, "name": "Chess960 Initialized Correctly, 50 times."},
            {"runnable": PositionTestSuite.test3, "name": "Double Bongcloud Initialized Correctly."},
            {"runnable": PositionTestSuite.test4, "name": "Dutch Defense: Classical Variation Initialized Correctly."},
            {"runnable": PositionTestSuite.test5, "name": "Scholar's Mate Initialized Correctly."},
            {"runnable": PositionTestSuite.test6, "name": "En Passant Test Initialized Correctly (1. c4 e5 2. c5 d5)"},
            {"runnable": PositionTestSuite.test7, "name": "Standard Position.next('e4') is actually 1. e4"}
        ]
    def test1():
        pos = Position.fromStartingPosition()        
        assert(pos.boardState != None)
        assert(pos.gameStatus.isWhiteToMove())
        assert(pos.castlingRights == CastlingRights.fromAllTrue())
        assert(pos.enPassantPawn == Vector.fromNonExistent())
        assert(pos.halfClock == 0)
        assert(pos.fullClock == 1)

        assert(pos.pieceAt(Vector.fromAN("e1")) == "K")
        assert(pos.pieceAt(Vector.fromAN("d1")) == "Q")
        assert(pos.pieceAt(Vector.fromAN("a2")) == "P")
        assert(pos.pieceAt(Vector.fromAN("a8")) == "r")

        return True
    def test2():
        for i in range(0, 50):
            pos = Position.fromChess960()
            assert(pos != None)
            assert(pos.boardState != None)
            assert(pos.enPassantPawn == Vector.fromNonExistent())
        return True
    def test3():
        pos = Position.fromFEN("rnbq1bnr/ppppkppp/8/4p3/4P3/8/PPPPKPPP/RNBQ1BNR w - - 0 1")
        assert(pos.boardState != None)
        assert(pos.gameStatus.isWhiteToMove())
        assert(pos.castlingRights == CastlingRights.fromFEN("-"))
        assert(pos.enPassantPawn == Vector.fromNonExistent())
        return True
    def test4():
        pos = Position.fromFEN("rnbq1rk1/ppp1b1pp/3ppn2/5p2/2PP4/5NP1/PP2PPBP/RNBQ1RK1 w - - 0 7")
        assert(pos.boardState != None)
        assert(pos.gameStatus.isWhiteToMove())
        assert(pos.castlingRights == CastlingRights.fromFEN("-"))
        assert(pos.enPassantPawn == Vector.fromNonExistent())
        return True
    def test5():
        pos = Position.fromFEN("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 1")
        assert(pos.boardState != None)
        assert(pos.gameStatus.isWhiteToMove())
        assert(pos.castlingRights == CastlingRights.fromAllTrue())
        assert(pos.enPassantPawn == Vector.fromNonExistent())
        return True
    def test6():
        pos = Position.fromFEN("rnbqkbnr/ppp2ppp/8/2Ppp3/8/8/PP1PPPPP/RNBQKBNR w KQkq d6 0 3")
        assert(pos.boardState != None)
        assert(pos.gameStatus.isWhiteToMove())
        assert(pos.castlingRights == CastlingRights.fromAllTrue())
        assert(pos.enPassantPawn == Vector.fromAlgebreicNotation("d6"))
        return True
    def test7():
        pos = Position.fromStartingPosition()
        move = Move.fromAN("e4")
        move.source = Vector.fromAN("e2")
        nextPos = pos.next(move)
        assert(nextPos.pieceAt(Vector.fromAN("e4")) == "P")
        return True
