from __future__ import annotations
from typing import Optional
from vector import Vector


class Move():
    def __init__(
            self, 
            pieceType: str = "", 
            source: Optional[Vector] = None, 
            destination: Optional[Vector] = None, 
            isCapture: bool = False, 
            isCheck: bool = False, 
            isCheckmate: bool = False, 
            promotionPiece: Optional[str] = None):
        self.pieceType = pieceType
        self.source = source
        self.destination = destination
        self.isCapture = isCapture
        self.isCheck = isCheck
        self.isCheckmate = isCheckmate
        self.promotionPiece = promotionPiece

    def __repr__(self):
        return self.toString()

    def clone(self) -> Move:
        return Move(
            self.pieceType,
            self.source,
            self.destination,
            self.isCapture,
            self.isCheck,
            self.isCheckmate,
            self.promotionPiece
        )

    def toString(self) -> str:
        return "Move %s%s%s%s (%s%s)" % (
            self.pieceType,
            self.source.toAN() if self.source else "None",
            "x" if self.isCapture else "->",
            self.destination.toAN() if self.destination else "None",
            "+" if self.isCheck else "",
            "#" if self.isCheckmate else ""
        )

    def setSource(self, vector: Vector) -> Move:
        self.source = vector
        return self

