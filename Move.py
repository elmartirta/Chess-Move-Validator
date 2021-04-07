import re
from vector2D import Vector2D

class Move():
    def __init__(self, pieceType, sourceFile, sourceRank, destination, isCapture, isCheck, isCheckmate, promotionPiece):
        self.pieceType = pieceType
        self.sourceFile = sourceFile
        self.sourceRank = int(sourceRank) if sourceRank else None
        self.destination = destination
        self.isCapture = isCapture 
        self.isCheck = isCheck
        self.isCheckmate = isCheckmate
        self.promotionPiece = promotionPiece
    def clone(self):
        return Move(
            self.pieceType,
            self.sourceFile,
            self.sourceRank,
            self.destination,
            self.isCapture,
            self.isCheck,
            self.isCheckmate,
            self.promotionPiece
        )
    def color(self):
        return "black" if self.pieceType.isupper() else "white"
    def setSource(self, cartesianVector):
        self.sourceFile = cartesianVector.y
        self.sourceRank = cartesianVector.x
        return self
    def fromString(string):
        return Move.fromAN(string)
    def fromAN(string):
        return Move.fromAlgebreicNotation(string)
    def fromAlgebreicNotation(string):
        pieceType = string[0] if len(string) >= 1 and (string[0] in "RNBQKP") else "P"
        sourceFile = None
        sourceRank = None
        destination = None
        isCapture = "x" in string
        isCheck = "+" in string
        isCheckmate = "#" in string
        promotionPiece = None
        
        if re.fullmatch("[RNBQKP]x*[a-z]\d[+#]*", string):
            #Parse Moves like Ke2, Be4+, Be4#
            destination = string.replace("x", "")[1:3]
        elif re.fullmatch("[RNBQKP][a-z]x*[a-z]\d[+#]*", string):
            #Parse moves like Rae4, etc
            sourceFile = string[1]
            destination = string.replace("x", "")[2:4]
        elif re.fullmatch("[RNBQKP]\dx*[a-z]\d[+#]*", string):
            #Parse moves like R1e4, etc
            sourceRank = string[1]
            destination = string.replace("x", "")[2:4]
        elif re.fullmatch("[RNBQKP][a-z]\dx*[a-z]\d[+#]*", string):
            #Parse moves like Qa1e4, etc
            sourceFile = string[1]
            sourceRank = string[2]
            destination = string.replace("x", "")[3:5]
        elif re.fullmatch("[a-z]\d[+#]*", string):
            #Parse moves like e4, 
            pieceType = "P"
            destination = string[0:2]
        elif re.fullmatch("[a-z]x[a-z]\d[+#]*", string):
            #Parse moves like dxe4
            pieceType = "P"
            sourceFile = string[0]
            destination = string[2:4]
        elif re.fullmatch("[a-z]8=[RNBQ][+#]*", string):
            #Parse moves like a8=Q
            pieceType = "P"
            destination = string[0:2]
            promotionPiece = string[3]
        elif re.fullmatch("[a-z]x[a-z]8=[RNBQ][+#]*", string):
            #Parse moves like dxa8=Q
            pieceType = "P"
            destination = string[2:4]
            promotionPiece = string[5]
        elif re.fullmatch("o-o-o", string):
            raise MoveParsingError("Long Castling is not implemented yet.")
        elif re.fullmatch("o-o", string):
            raise MoveParsingError("Castling is not implemented yet.")
        else:
            raise MoveParsingError("Move does not match any valid regex expression", string)
        destination = Vector2D.fromAN(destination)
        return Move(pieceType, sourceFile, sourceRank, destination, isCapture, isCheck, isCheckmate, promotionPiece)
    def toString(self):
        return "Move : %s %s%s -> %s [Capt: %s, Check: %s, Mate: %s]" % (
            self.pieceType,
            self.sourceFile,
            self.sourceRank,
            self.destination.toAN(),
            self.isCapture,
            self.isCheck,
            self.isCheckmate
        )
class MoveParsingError(ValueError):
    def __init__(self, message, moveString):
        super().__init__("The move %s cannot be parsed:\n\t%s" %(moveString, message))
