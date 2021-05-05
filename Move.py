import re
from vector import Vector

class Move():
    def __init__(
            self, 
            pieceType, 
            source, 
            destination, 
            isCapture, 
            isCheck, 
            isCheckmate, 
            promotionPiece):
        self.pieceType = pieceType
        self.source = source
        self.destination = destination
        self.isCapture = isCapture 
        self.isCheck = isCheck
        self.isCheckmate = isCheckmate
        self.promotionPiece = promotionPiece

    def __repr__(self):
        return self.toString()

    def clone(self):
        return Move(
            self.pieceType,
            self.source,
            self.destination,
            self.isCapture,
            self.isCheck,
            self.isCheckmate,
            self.promotionPiece
        )

    def fromAN(string):
        return Move.fromAlgebreicNotation(string)

    def fromAlgebreicNotation(string):
        pieceType = string[0] if len(string) >= 1 and (string[0] in "RNBQKP") else "P"
        source = None
        destination = None
        isCapture = "x" in string
        isCheck = "+" in string
        isCheckmate = "#" in string
        promotionPiece = None
        
        basicMatch = re.fullmatch("^([RNBKQP])([a-w])?(\d)?(x)?([a-w]\d)[+#]?$", string)
        if basicMatch:
            pieceType = basicMatch.group(1)
            sourceFile = basicMatch.group(2) if basicMatch.group(2) else ""
            sourceRank = basicMatch.group(3) if basicMatch.group(3) else ""
            source = Vector.fromAN(sourceFile + sourceRank)
            destination = Vector.fromAN(basicMatch.group(5))
        else: 
            pawnMatch = re.fullmatch("(([a-w])(x))?([a-w]\d)(=([RNBQ]))?[+#]?", string)
            if pawnMatch:
                source = Vector.fromAN(pawnMatch.group(2))
                destination = Vector.fromAN(pawnMatch.group(4))
                promotionPiece = pawnMatch.group(6)
            else:
                raise MoveParsingError(string, "Move does not match any valid regex expression")
        return Move(pieceType, source, destination, isCapture, isCheck, isCheckmate, promotionPiece)

    def fromEmpty():
        #TODO: CODE SMELL - Unused code? What is this? Why would I use this?
        return Move(
            "",
            Vector.fromNonExistent(),
            Vector.fromNonExistent(),
            False,
            False,
            False,
            Vector.fromNonExistent()
        )

    def toString(self):
        return "Move %s%s%s%s (%s%s)" % (
            self.pieceType,
            self.source.toAN() if self.source else "None",
            "x" if self.isCapture else "->",
            self.destination.toAN(),
            "+" if self.isCheck else "",
            "#" if self.isCheckmate else ""
        )

    def setSource(self, vector):
        self.source = vector
        return self

class MoveParsingError(ValueError):
    def __init__(self, moveString, message):
        super().__init__("The move %s cannot be parsed:\n\t%s" %(moveString, message))