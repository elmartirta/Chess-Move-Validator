from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Optional
from vector import Vector


@dataclass
class CastlingMove():
    pieceType: str
    source: Optional[Vector]
    destination: Optional[Vector]
    isCapture: bool
    isCheck: bool
    isCheckmate: bool 
    promotionPiece: Optional[Vector]
    isKingsideCastling: bool
    rookLocation: Optional[Vector]
    
    def clone(self):
        return replace(self)

    def __repr__(self) -> str:
        return "Castling"+super().__repr__()

    def midStep(self) -> Vector:
        if self.source is None: raise ValueError
        return self.source + (Vector(1,0) if self.isKingsideCastling else Vector(-1,0))


