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

    def clone(self) -> CastlingMove:
        return CastlingMove(
            self.pieceType,
            self.source,
            self.destination,
            self.isCapture,
            self.isCheck,
            self.isCheckmate,
            None,
            self.castlingDirection,
            self.rookLocation
        )

    @classmethod
    def fromAN(cls, string: str) -> CastlingMove | Move:
        return cls.fromAlgebreicNotation(string)

    @classmethod
    def fromAlgebreicNotation(cls, string: str) -> CastlingMove | Move:
        #TODO: SMELL - Misplaced Factory - This Algebreic Notatition -> Move/Castling Move
        #Logic, could be placed in a much better location. Perhaps a dedicated static method or
        #factory class that takes a string and returns a castling move or move. This way, you can
        #more easily create classes such as "Unfinished Move" or "UnfinishedCastlingMove" that
        #contain Optional[Vector] values, when proper CastlingMoves contain Vector values.
        castlingMatch = re.fullmatch("O-O(-O)?([+#])?", string)
        if castlingMatch:
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

    def isKingsideCastling(self) -> bool:
        return self.castlingDirection == CastlingDirection.KINGSIDE

    def toString(self) -> str:
        return "Castling"+super().toString()

    def midStep(self) -> Vector:
        if self.source is None: raise ValueError
        return self.source + (Vector(1,0) if self.isKingsideCastling() else Vector(-1,0))

class CastlingDirection(Enum):
    KINGSIDE = 1
    QUEENSIDE = 2
