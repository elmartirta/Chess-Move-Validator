from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Optional
from vector import Vector


@dataclass
class Move():
    pieceType: str
    source: Optional[Vector]
    destination: Optional[Vector]
    isCapture: bool = False
    isCheck: bool = False
    isCheckmate: bool = False
    promotionPiece: Optional[str] = None

    def clone(self):
        return replace(self)

    def __repr__(self):
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

