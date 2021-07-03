from __future__ import annotations
from dataclasses import dataclass

@dataclass
class CastlingRights():
    whiteKingSide: bool = True
    whiteQueenSide: bool = True
    blackKingSide: bool = True
    blackQueenSide: bool = True
    
    @classmethod
    def fromFEN(cls, string: str) -> CastlingRights:
        return cls(
            "K" in string,
            "Q" in string,
            "k" in string,
            "q" in string
        )