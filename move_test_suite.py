from move import Move
from vector2D import Vector2D

class MoveTestSuite():
    def getTests():
        return [
            {"runnable": MoveTestSuite.test1, "name": "Moves like : Ra1, Ra1+, Ra1#, Rxa1+"},
            {"runnable": MoveTestSuite.test2, "name": "Moves like : Rba1, Rba1+, etc"},
            {"runnable": MoveTestSuite.test3, "name": "Moves like : R1a2, R1a2+, etc"}
        ]
    def test1():
        m = Move.fromAN("Ra1")
        assert(m.destination == Vector2D.fromAN("a1") and m.pieceType == "R")
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)
        m = Move.fromAN("Ba1+")
        assert(m.destination == Vector2D.fromAN("a1") and m.pieceType == "B")
        assert(m.isCapture == False)
        assert(m.isCheck == True)
        assert(m.isCheckmate == False)
        m = Move.fromAN("Rxa1#")
        assert(m.destination == Vector2D.fromAN("a1") and m.pieceType == "R")
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)
        m = Move.fromAN("Pxa1#")
        assert(m.destination == Vector2D.fromAN("a1") and m.pieceType == "P")
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)        
        return True
    def test2():
        m = Move.fromAN("Rba1")
        assert(m.destination == Vector2D.fromAN("a1") and m.pieceType == "R" and m.sourceFile == "b")
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)
        m = Move.fromAN("Qbxa1#")
        assert(m.destination == Vector2D.fromAN("a1") and m.pieceType == "Q" and m.sourceFile == "b")
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)
        m = Move.fromAN("Bbxa1#")
        assert(m.destination == Vector2D.fromAN("a1") and m.pieceType == "B" and m.sourceFile == "b")
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)
        return True
    def test3():
        m = Move.fromAN("R1a1")
        assert(m.destination == Vector2D.fromAN("a1") and m.pieceType == "R" and m.sourceRank == 1)
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)
        m = Move.fromAN("Q8xa1#")
        assert(m.destination == Vector2D.fromAN("a1") and m.pieceType == "Q" and m.sourceRank == 8)
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)
        m = Move.fromAN("B4xa1#")
        assert(m.destination == Vector2D.fromAN("a1") and m.pieceType == "B" and m.sourceRank == 4)
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)
        return True