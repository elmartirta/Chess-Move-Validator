from move import Move
from vector import Vector

class MoveTestSuite():
    def getTests():
        return [
            {"runnable": MoveTestSuite.Ra1, "name": "Moves like : Ra1, Ra1+, Ra1#, Rxa1+"},
            {"runnable": MoveTestSuite.Rba1, "name": "Moves like : Rba1, Rba1+, etc"},
            {"runnable": MoveTestSuite.R1a1, "name": "Moves like : R1a2, R1a2+, etc"},
            {"runnable": MoveTestSuite.Rb1a1, "name": "Moves like : Rb1a2, Rb1a2+, Rb1a2#, etc"},
            {"runnable": MoveTestSuite.e4, "name": "Moves like : e4, e4#, e4+"},
            {"runnable": MoveTestSuite.dxe4, "name": "Moves like : dxe4, dxe5#, dxe3+"},
            {"runnable": MoveTestSuite.h8Q, "name": "Moves like : h8=Q, h8=Q+, h8=N#"},
        ]

    def Ra1():
        m = Move.fromAN("Ra1")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "R")
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)

        m = Move.fromAN("Ba1+")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "B")
        assert(m.isCapture == False)
        assert(m.isCheck == True)
        assert(m.isCheckmate == False)

        m = Move.fromAN("Rxa1#")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "R")
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)

        m = Move.fromAN("Pxa1#")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "P")
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)   

        return True

    def Rba1():
        m = Move.fromAN("Rba1")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "R")
        assert(m.source == Vector.fromAN("b"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)

        m = Move.fromAN("Qbxa1#")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "Q")
        assert(m.source == Vector.fromAN("b"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)

        m = Move.fromAN("Bbxa1#")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "B")
        assert(m.source == Vector.fromAN("b"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)

        return True

    def R1a1():
        m = Move.fromAN("R1a1")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "R")
        assert(m.source == Vector.fromAN("1"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)

        m = Move.fromAN("Q8xa1#")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "Q")
        assert(m.source == Vector.fromAN("8"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)

        m = Move.fromAN("B4xa1#")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "B")
        assert(m.source == Vector.fromAN("4"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)

        return True

    def Rb1a1():
        m = Move.fromAN("Rb1a2")
        assert(m.pieceType == "R")
        assert(m.destination == Vector.fromAN("a2"))
        assert(m.source == Vector.fromAN("b1"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)

        m = Move.fromAN("Ba1xh8#")
        assert(m.pieceType == "B")
        assert(m.destination == Vector.fromAN("h8"))
        assert(m.source == Vector.fromAN("a1"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)

        m = Move.fromAN("Ba2h8+")
        assert(m.pieceType == "B")
        assert(m.destination == Vector.fromAN("h8"))
        assert(m.source == Vector.fromAN("a2"))
        assert(m.isCapture == False)
        assert(m.isCheck == True)
        assert(m.isCheckmate == False)

        return True

    def e4():
        m = Move.fromAN("e4")        
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("e4"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)

        m = Move.fromAN("e4+")        
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("e4"))
        assert(m.isCapture == False)
        assert(m.isCheck == True)
        assert(m.isCheckmate == False)

        return True

    def dxe4():
        m = Move.fromAN("dxe4#")        
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("e4"))
        assert(m.source == Vector.fromAN("d"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)

        return True

    def h8Q():
        m = Move.fromAN("h8=Q")
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("h8"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)
        assert(m.promotionPiece == "Q")

        m = Move.fromAN("a8=R+")
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("a8"))
        assert(m.isCapture == False)
        assert(m.isCheck == True)
        assert(m.isCheckmate == False)
        assert(m.promotionPiece == "R")

        m = Move.fromAN("f8=N#")
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("f8"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)
        assert(m.promotionPiece == "N")

        return True

    def fxh8Q():
        m = Move.fromAN("bxc8=B")
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("c8"))
        assert(m.source == Vector.fromAN("c"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)
        assert(m.promotionPiece == "B")

        m = Move.fromAN("bxa8=Q+")
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("a8"))
        assert(m.source == Vector.fromAN("b"))
        assert(m.isCapture == False)
        assert(m.isCheck == True)
        assert(m.isCheckmate == False)
        assert(m.promotionPiece == "Q")

        m = Move.fromAN("gxh8=R#")
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("h8"))
        assert(m.source == Vector.fromAN("g"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)
        assert(m.promotionPiece == "R")
        
        return True