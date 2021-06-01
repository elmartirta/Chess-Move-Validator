from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Optional
from vector import UnfinishedVector, Vector


@dataclass
class Move():
    pieceType: str
    source: Vector
    destination: Vector
    isCapture: bool = False
    isCheck: bool = False
    isCheckmate: bool = False
    promotionPiece: Optional[str] = None

    def clone(self):
        return replace(self)

    def __repr__(self):
        return "Move %s%s%s%s (%s%s)" % (
            self.pieceType,
            self.source.toAN(),
            "x" if self.isCapture else "->",
            self.destination.toAN(),
            "+" if self.isCheck else "",
            "#" if self.isCheckmate else ""
        )

    def setSource(self, vector: Vector) -> Move:
        self.source = vector
        return self

@dataclass
class UnfinishedMove():
    pieceType: str
    source: Optional[Vector | UnfinishedVector]
    destination: Vector
    isCapture: bool = False
    isCheck: bool = False
    isCheckmate: bool = False
    promotionPiece: Optional[str] = None

    def clone(self):
        return replace(self)

    def __repr__(self):
        return "Unfinished Move %s%s%s%s (%s%s)" % (
            self.pieceType,
            self.source.toAN() if self.source else "None",
            "x" if self.isCapture else "->",
            self.destination.toAN() if self.destination else "None",
            "+" if self.isCheck else "",
            "#" if self.isCheckmate else ""
        )

    def setSource(self, vector: Vector) -> UnfinishedMove:
        self.source = vector
        return self

    def complete(self, source: Vector) -> Move:
        return Move(
            self.pieceType,
            source,
            self.destination,
            self.isCapture,
            self.isCheck,
            self.isCheckmate,
            self.promotionPiece
        )
