from notation_parser import NotationParser
from vector import Vector

class MoveTestSuite():
    @staticmethod
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

    @staticmethod
    def Ra1():
        m = NotationParser.parseAlgebreicNotation("Ra1")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "R")
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)

        m = NotationParser.parseAlgebreicNotation("Ba1+")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "B")
        assert(m.isCapture == False)
        assert(m.isCheck == True)
        assert(m.isCheckmate == False)

        m = NotationParser.parseAlgebreicNotation("Rxa1#")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "R")
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)

        m = NotationParser.parseAlgebreicNotation("Pxa1#")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "P")
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)   

        return True

    @staticmethod
    def Rba1():
        m = NotationParser.parseAlgebreicNotation("Rba1")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "R")
        assert(m.source == Vector.fromAN("b"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)

        m = NotationParser.parseAlgebreicNotation("Qbxa1#")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "Q")
        assert(m.source == Vector.fromAN("b"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)

        m = NotationParser.parseAlgebreicNotation("Bbxa1#")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "B")
        assert(m.source == Vector.fromAN("b"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)

        return True

    @staticmethod
    def R1a1():
        m = NotationParser.parseAlgebreicNotation("R1a1")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "R")
        assert(m.source == Vector.fromAN("1"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)

        m = NotationParser.parseAlgebreicNotation("Q8xa1#")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "Q")
        assert(m.source == Vector.fromAN("8"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)

        m = NotationParser.parseAlgebreicNotation("B4xa1#")
        assert(m.destination == Vector.fromAN("a1"))
        assert(m.pieceType == "B")
        assert(m.source == Vector.fromAN("4"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)

        return True

    @staticmethod
    def Rb1a1():
        m = NotationParser.parseAlgebreicNotation("Rb1a2")
        assert(m.pieceType == "R")
        assert(m.destination == Vector.fromAN("a2"))
        assert(m.source == Vector.fromAN("b1"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)

        m = NotationParser.parseAlgebreicNotation("Ba1xh8#")
        assert(m.pieceType == "B")
        assert(m.destination == Vector.fromAN("h8"))
        assert(m.source == Vector.fromAN("a1"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)

        m = NotationParser.parseAlgebreicNotation("Ba2h8+")
        assert(m.pieceType == "B")
        assert(m.destination == Vector.fromAN("h8"))
        assert(m.source == Vector.fromAN("a2"))
        assert(m.isCapture == False)
        assert(m.isCheck == True)
        assert(m.isCheckmate == False)

        return True

    @staticmethod
    def e4():
        m = NotationParser.parseAlgebreicNotation("e4")        
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("e4"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)

        m = NotationParser.parseAlgebreicNotation("e4+")        
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("e4"))
        assert(m.isCapture == False)
        assert(m.isCheck == True)
        assert(m.isCheckmate == False)

        return True

    @staticmethod
    def dxe4():
        m = NotationParser.parseAlgebreicNotation("dxe4#")        
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("e4"))
        assert(m.source == Vector.fromAN("d"))
        assert(m.isCapture == True)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)

        return True

    @staticmethod
    def h8Q():
        m = NotationParser.parseAlgebreicNotation("h8=Q")
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("h8"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)
        assert(m.promotionPiece == "Q")

        m = NotationParser.parseAlgebreicNotation("a8=R+")
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("a8"))
        assert(m.isCapture == False)
        assert(m.isCheck == True)
        assert(m.isCheckmate == False)
        assert(m.promotionPiece == "R")

        m = NotationParser.parseAlgebreicNotation("f8=N#")
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("f8"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)
        assert(m.promotionPiece == "N")

        return True

    @staticmethod
    def fxh8Q():
        m = NotationParser.parseAlgebreicNotation("bxc8=B")
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("c8"))
        assert(m.source == Vector.fromAN("c"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == False)
        assert(m.promotionPiece == "B")

        m = NotationParser.parseAlgebreicNotation("bxa8=Q+")
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("a8"))
        assert(m.source == Vector.fromAN("b"))
        assert(m.isCapture == False)
        assert(m.isCheck == True)
        assert(m.isCheckmate == False)
        assert(m.promotionPiece == "Q")

        m = NotationParser.parseAlgebreicNotation("gxh8=R#")
        assert(m.pieceType == "P")
        assert(m.destination == Vector.fromAN("h8"))
        assert(m.source == Vector.fromAN("g"))
        assert(m.isCapture == False)
        assert(m.isCheck == False)
        assert(m.isCheckmate == True)
        assert(m.promotionPiece == "R")
        
        return True