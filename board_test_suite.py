from typing import List
from verifier.vector import Vector
from verifier.board import Board


class BoardTestSuite():
    @classmethod
    def getTests(cls):
        return[
            {"runnable": cls.initializeEmptyBoard, "name": "Initialize a Board object"},
            {"runnable": cls.boardHasSquares, "name": "Board() contains an 8x8 .squares matrix"},
            {"runnable": cls.emptyBoardFromFen, "name": "Initialize a Board object"},
            {"runnable": cls.startingBoardFromFEN, "name": "Initialize a Board object"},
            {"runnable": cls.boardEquality, "name": "Is able to compare boards"},
            {"runnable": cls.canSee, "name": "Checking if pieces can see others"},
        ]
    
    @staticmethod
    def initializeEmptyBoard():
        board = Board()
        return True

    @staticmethod
    def boardHasSquares():
        squares = Board()._squares
        assert(squares)
        assert(len(squares) == 8), squares
        assert(all([len(row) == 8 for row in squares])), squares
        assert(all([(square == '-' for square in row) for row in squares])), squares
        return True

    @staticmethod    
    def emptyBoardFromFen():
        emptyBoard = Board.fromFEN("8/8/8/8/8/8/8/8")
        assert(emptyBoard._squares == Board()._squares)
        return True
    
    @staticmethod
    def startingBoardFromFEN():
        startingBoard = Board.fromFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        assert(startingBoard._squares[0] == [s for s in "RNBQKBNR"]), startingBoard._squares[0]
        assert(startingBoard._squares[1] == [s for s in "PPPPPPPP"]), startingBoard._squares[1]
        assert(startingBoard._squares[6] == [s for s in "pppppppp"]), startingBoard._squares[6]
        assert(startingBoard._squares[7] == [s for s in "rnbqkbnr"]), startingBoard._squares[7]
        return True
    
    @staticmethod
    def boardEquality():
        assert(Board() == Board())
        startingPos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        assert(Board.fromFEN(startingPos) == Board.fromFEN(startingPos))
        return True

    @staticmethod
    def canSee():
        starBoard = Board.fromFEN("8/3q3k/1Q1Q1Q2/8/qQ1q1Qq1/8/1Q1Q1Q1K/3q4")
        attacker = Vector.fromAN("d4")

        assert(starBoard.pieceCanSee(attacker, Vector.fromAN("b2")))
        assert(starBoard.pieceCanSee(attacker, Vector.fromAN("d2")))
        assert(starBoard.pieceCanSee(attacker, Vector.fromAN("f2")))
        assert(starBoard.pieceCanSee(attacker, Vector.fromAN("b4")))
        assert(starBoard.pieceCanSee(attacker, Vector.fromAN("f4")))
        assert(starBoard.pieceCanSee(attacker, Vector.fromAN("b6")))
        assert(starBoard.pieceCanSee(attacker, Vector.fromAN("d6")))
        assert(starBoard.pieceCanSee(attacker, Vector.fromAN("f6")))
        
        assert(not starBoard.pieceCanSee(attacker, Vector.fromAN("d1")))
        assert(not starBoard.pieceCanSee(attacker, Vector.fromAN("a4")))
        assert(not starBoard.pieceCanSee(attacker, Vector.fromAN("g4")))
        assert(not starBoard.pieceCanSee(attacker, Vector.fromAN("d7")))
        return True