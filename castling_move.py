from vector import Vector
from move import Move
from enum import Enum
import re


class CastlingMove(Move):
    def __init__(
            self, 
            pieceType, 
            source, 
            destination, 
            isCapture, 
            isCheck, 
            isCheckmate, 
            promotionPiece, 
            castlingDirection, 
            rookLocation):
        super().__init__(
            pieceType, 
            source, 
            destination, 
            isCapture, 
            isCheck, 
            isCheckmate, 
            promotionPiece)
        self.castlingDirection = castlingDirection
        self.rookLocation = rookLocation

    def clone(self):
        return CastlingMove(
            self.pieceType,
            self.source,
            self.destination,
            self.isCapture,
            self.isCheck,
            self.isCheckmate,
            self.promotionPiece,
            self.castlingDirection,
            self.rookLocation
        )

    def fromAN(string):
        return CastlingMove.fromAlgebreicNotation(string)

    def fromAlgebreicNotation(string):
        castlingMatch = re.fullmatch("O-O(-O)?([+#])?", string)
        if castlingMatch:
            e = Move.fromEmpty()
            return CastlingMove(
                "K", 
                e.source, 
                e.destination, 
                "x" in string, 
                "+" in string, 
                "#" in string, 
                e.promotionPiece, 
                CastlingDirection.QUEENSIDE if castlingMatch.group(1) else CastlingDirection.KINGSIDE, 
                Vector.fromNonExistent())
        else:
            return Move.fromAlgebreicNotation(string)

    def isKingsideCastling(self):
        return self.castlingDirection == CastlingDirection.KINGSIDE

    def toString(self):
        return "Castling"+super().toString()

    def midStep(self):
        return self.source + (Vector(1,0) if self.isKingsideCastling() else Vector(-1,0))

class CastlingDirection(Enum):
    KINGSIDE = 1
    QUEENSIDE = 2
