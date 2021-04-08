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
        
        basicMatch = re.fullmatch("^([RNBKQP])([a-w])?(\d)?(x)?([a-w]\d)[+#]?$", string)
        if basicMatch:
            pieceType = basicMatch.group(1)
            sourceFile = basicMatch.group(2)
            sourceRank = basicMatch.group(3)
            destination = basicMatch.group(5)
        else: 
            pawnMatch = re.fullmatch("(([a-w])(x))?([a-w]\d)(=([RNBQ]))?[+#]?", string)
            if pawnMatch:
                sourceFile = pawnMatch.group(2)
                destination = pawnMatch.group(4)
                promotionPiece = pawnMatch.group(6)
            elif re.fullmatch("o-o-o", string):
                raise MoveParsingError(string, "Long Castling is not implemented yet.")
            elif re.fullmatch("o-o", string):
                raise MoveParsingError(string, "Castling is not implemented yet.")
            else:
                raise MoveParsingError(string, "Move does not match any valid regex expression")
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
    def __init__(self, moveString, message):
        super().__init__("The move %s cannot be parsed:\n\t%s" %(moveString, message))
