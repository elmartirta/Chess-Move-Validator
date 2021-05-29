from __future__ import annotations
from typing import Optional
from vector import Vector
from move import Move
from enum import Enum


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
