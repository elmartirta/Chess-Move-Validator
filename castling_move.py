from __future__ import annotations
from typing import Optional
from vector import Vector
from move import Move
from enum import Enum
import re


class CastlingMove(Move):
    def __init__(
            self, 
            pieceType: str, 
            source: Optional[Vector], 
            destination: Optional[Vector], 
            isCapture: bool, 
            isCheck: bool, 
            isCheckmate: bool, 
            promotionPiece: None, 
            castlingDirection: CastlingDirection, 
            rookLocation: Optional[Vector]):
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

    @classmethod
    def fromAN(cls, string: str):
        return cls.fromAlgebreicNotation(string)

    @classmethod
    def fromAlgebreicNotation(cls, string: str):
        castlingMatch = re.fullmatch("O-O(-O)?([+#])?", string)
        if castlingMatch:
            e = Move()
            return cls(
                "K", 
                None, 
                None, 
                "x" in string, 
                "+" in string, 
                "#" in string, 
                None, 
                CastlingDirection.QUEENSIDE if castlingMatch.group(1) else CastlingDirection.KINGSIDE, 
                None)
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
