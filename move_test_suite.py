from move import Move
from vector2D import Vector2D

class MoveTestSuite():
    def getTests():
        return [
            {"runnable": MoveTestSuite.test1, "name": "Moves like : Ra1, Ra1+, Ra1#, Rxa1+"},
            {"runnable": MoveTestSuite.test2, "name": "Moves like : Rba1, Rba1+, etc"},
            {"runnable": MoveTestSuite.test3, "name": "Moves like : R1a2, R1a2+, etc"},
            {"runnable": MoveTestSuite.test4, "name": "Moves like : Rb1a2, Rb1a2+, Rb1a2#, etc"},
            {"runnable": MoveTestSuite.test5, "name": "Moves like : e4, e4#, e4+"},
            {"runnable": MoveTestSuite.test6, "name": "Moves like : dxe4, dxe5#, dxe3+"},
            {"runnable": MoveTestSuite.test7, "name": "Moves like : h8=Q, h8=Q+, h8=N#"}
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
        assert(m.destination == Vector2D.fromAN("a1") and m.pieceType == "R" and m.source == Vector2D.fromAN("b"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)
        m = Move.fromAN("Qbxa1#")
        assert(m.destination == Vector2D.fromAN("a1") and m.pieceType == "Q" and m.source == Vector2D.fromAN("b"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)
        m = Move.fromAN("Bbxa1#")
        assert(m.destination == Vector2D.fromAN("a1") and m.pieceType == "B" and m.source == Vector2D.fromAN("b"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)
        return True
    def test3():
        m = Move.fromAN("R1a1")
        assert(m.destination == Vector2D.fromAN("a1") and m.pieceType == "R" and m.source == Vector2D.fromAN("1"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)
        m = Move.fromAN("Q8xa1#")
        assert(m.destination == Vector2D.fromAN("a1") and m.pieceType == "Q" and m.source == Vector2D.fromAN("8"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)
        m = Move.fromAN("B4xa1#")
        assert(m.destination == Vector2D.fromAN("a1") and m.pieceType == "B" and m.source == Vector2D.fromAN("4"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)
        return True
    def test4():
        m = Move.fromAN("Rb1a2")
        assert(m.pieceType == "R" and m.destination == Vector2D.fromAN("a2") and m.source == Vector2D.fromAN("b1"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)
        m = Move.fromAN("Ba1xh8#")
        assert(m.pieceType == "B" and m.destination == Vector2D.fromAN("h8") and m.source == Vector2D.fromAN("a1"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)
        m = Move.fromAN("Ba2h8+")
        assert(m.pieceType == "B" and m.destination == Vector2D.fromAN("h8") and m.source == Vector2D.fromAN("a2"))
        assert(m.isCapture == False)
        assert(m.isCheck == True)
        assert(m.isCheckmate == False)
        return True
    def test5():
        m = Move.fromAN("e4")        
        assert(m.pieceType == "P" and m.destination == Vector2D.fromAN("e4"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)
        m = Move.fromAN("e4+")        
        assert(m.pieceType == "P" and m.destination == Vector2D.fromAN("e4"))
        assert(m.isCapture == False)
        assert(m.isCheck == True)
        assert(m.isCheckmate == False)
        return True
    def test6():
        m = Move.fromAN("dxe4#")        
        assert(m.pieceType == "P" and m.destination == Vector2D.fromAN("e4") and m.source == Vector2D.fromAN("d"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)
        return True
    def test7():
        m = Move.fromAN("h8=Q")
        assert(m.pieceType == "P" and m.destination == Vector2D.fromAN("h8"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)
        assert(m.promotionPiece == "Q")
        m = Move.fromAN("a8=R+")
        assert(m.pieceType == "P" and m.destination == Vector2D.fromAN("a8"))
        assert(m.isCapture == False)
        assert(m.isCheck == True)
        assert(m.isCheckmate == False)
        assert(m.promotionPiece == "R")
        m = Move.fromAN("f8=N#")
        assert(m.pieceType == "P" and m.destination == Vector2D.fromAN("f8"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)
        assert(m.promotionPiece == "N")
        return True
    def test8():
        m = Move.fromAN("bxc8=B")
        assert(m.pieceType == "P" and m.destination == Vector2D.fromAN("c8") and m.source == Vector2D.fromAN("c"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)
        assert(m.promotionPiece == "B")
        m = Move.fromAN("bxa8=Q+")
        assert(m.pieceType == "P" and m.destination == Vector2D.fromAN("a8") and m.source == Vector2D.fromAN("b"))
        assert(m.isCapture == False)
        assert(m.isCheck == True)
        assert(m.isCheckmate == False)
        assert(m.promotionPiece == "Q")
        m = Move.fromAN("gxh8=R#")
        assert(m.pieceType == "P" and m.destination == Vector2D.fromAN("h8") and m.source == Vector2D.fromAN("g"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)
        assert(m.promotionPiece == "R")
        return True