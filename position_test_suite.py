from position import *
from move import *
from vector import Vector


class PositionTestSuite():
    def getTests():
        return [
            {"runnable": PositionTestSuite.startPos, "name": "Chess Starting Position Initialized Correctly"},
            {"runnable": PositionTestSuite.chess960, "name": "Chess960 Initialized Correctly, 50 times."},
            {"runnable": PositionTestSuite.doblBong, "name": "Double Bongcloud Initialized Correctly."},
            {"runnable": PositionTestSuite.dutchDef, "name": "Dutch Defense: Classical Variation Initialized Correctly."},
            {"runnable": PositionTestSuite.scholMat, "name": "Scholar's Mate Initialized Correctly."},
            {"runnable": PositionTestSuite.enPassant, "name": "En Passant Test Initialized Correctly (1. c4 e5 2. c5 d5)"},
            {"runnable": PositionTestSuite.nextIsE4, "name": "Standard Position.next('e4') is actually 1. e4"}
        ]

    def startPos():
        pos = Position.fromStartingPosition()        
        assert(pos.squares != None)
        assert(pos.isWhiteToMove)
        assert(pos.castlingRights != None)
        assert(pos.enPassantPawn == Vector.fromNonExistent())
        assert(pos.halfClock == 0)
        assert(pos.fullClock == 1)

        assert(pos.pieceAt(Vector.fromAN("e1")) == "K")
        assert(pos.pieceAt(Vector.fromAN("d1")) == "Q")
        assert(pos.pieceAt(Vector.fromAN("a2")) == "P")
        assert(pos.pieceAt(Vector.fromAN("a8")) == "r")

        return True

    def chess960():
        for i in range(0, 50):
            pos = Position.fromChess960()
            assert(pos != None)
            assert(pos.squares != None)
            assert(pos.enPassantPawn == Vector.fromNonExistent())
        return True

    def doblBong():
        pos = Position.fromFEN("rnbq1bnr/ppppkppp/8/4p3/4P3/8/PPPPKPPP/RNBQ1BNR w - - 0 1")
        assert(pos.squares != None)
        assert(pos.isWhiteToMove)
        assert(pos.castlingRights == CastlingRights.fromFEN("-"))
        assert(pos.enPassantPawn == Vector.fromNonExistent())
        return True

    def dutchDef():
        pos = Position.fromFEN("rnbq1rk1/ppp1b1pp/3ppn2/5p2/2PP4/5NP1/PP2PPBP/RNBQ1RK1 w - - 0 7")
        assert(pos.squares != None)
        assert(pos.isWhiteToMove)
        assert(pos.castlingRights == CastlingRights.fromFEN("-"))
        assert(pos.enPassantPawn == Vector.fromNonExistent())
        return True

    def scholMat():
        pos = Position.fromFEN("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 1")
        assert(pos.squares != None)
        assert(pos.isWhiteToMove)
        assert(pos.castlingRights == CastlingRights.fromFEN("KQkq"))
        assert(pos.enPassantPawn == Vector.fromNonExistent())
        return True

    def enPassant():
        pos = Position.fromFEN("rnbqkbnr/ppp2ppp/8/2Ppp3/8/8/PP1PPPPP/RNBQKBNR w KQkq d6 0 3")
        assert(pos.squares != None)
        assert(pos.isWhiteToMove)
        assert(pos.castlingRights == CastlingRights.fromFEN("KQkq"))
        assert(pos.enPassantPawn == Vector.fromAlgebreicNotation("d6"))
        return True

    def nextIsE4():
        pos = Position.fromStartingPosition()
        move = Move.fromAN("e4")
        move.source = Vector.fromAN("e2")
        nextPos = pos.next(move)
        assert(nextPos.pieceAt(Vector.fromAN("e4")) == "P")
        return True