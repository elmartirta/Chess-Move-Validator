from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional


class Vector():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __radd__(self, other: Vector) -> Vector:
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: int) -> Vector:
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: int) -> Vector:
        return (self * scalar)

    def __eq__(self, other) -> bool:
        if self is None or other is None: return False
        if not isinstance(other, Vector): return False
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return "Vector(%s, %s)" % (str(self.x), str(self.y))

    @classmethod
    def fromANStrict(cls, text: str) -> Vector:
        vec = cls.parseAlgebreicNotation(text)
        if isinstance(vec, UnfinishedVector):
            raise ValueError
        return vec

    @classmethod
    def fromAN(cls, text: str) -> Vector | UnfinishedVector:
        return cls.parseAlgebreicNotation(text)

    @classmethod
    def parseAlgebreicNotation(cls, text: str) -> Vector | UnfinishedVector:
        if text is None:
            return UnfinishedVector(None, None)
        elif len(text) == 0:
            return UnfinishedVector(None, None)
        elif len(text) == 1:
            if text.isalpha():
                return UnfinishedVector(cls._alphaToX(text), None)
            else:
                return UnfinishedVector(None, cls._numericToY(text))
        elif len(text) == 2:
            return Vector(
                cls._alphaToX(text[0]), 
                cls._numericToY(text[1]))
        else:
            raise ANParsingError(text, "Length of the text is longer than 2")

    @staticmethod
    def _alphaToX(chr: str) -> int:
        return ord(chr.lower()) - 97
    
    @staticmethod
    def _xToAlpha(x: int) -> str:
        return str(x+97)

    @staticmethod
    def _numericToY(chr: str) -> int:
        return int(chr)-1

    @staticmethod
    def _yToNumeric(y: int) -> str:
        return chr(y + 1)

    def toAN(self) -> str:
        return self.toAlgebreicNotation()

    @classmethod
    def toAlgebreicNotation(cls, self) -> str:
        sourceRank = cls._xToAlpha(self.x)
        sourceFile = cls._yToNumeric(self.y)
        return sourceRank + sourceFile

    def plus(self, x: int, y: int) -> Vector:
        return Vector(self.x + x, self.y + y)

    def minus(self, x: int, y: int) -> Vector:
        return Vector(self.x - x, self.y - y) 

    def equals(self, x: int, y: int) -> bool:
        return self == Vector(x,y)

    def times(self, scalar: int) -> Vector:
        return self * scalar

    def toString(self) -> str:
        return str(self)

    def isInsideChessboard(self) -> bool:
        return self.x >= 0 and self.x <= 7 and self.y >= 0 and self.y <= 7

    def between(self, other: Vector) -> List[Vector]:
        return [self + delta for delta in (other - self).walk()]

    def walk(self) -> List[Vector]:
        deltas = []
        direction = Vector(
            ((1 if self.x > 0 else -1) if self.x != 0 else 0),
            ((1 if self.y > 0 else -1) if self.y != 0 else 0)
        )
        
        if abs(self.x) == abs(self.y) or self.x == 0 or self.y == 0:
            for deltaMagnitude in range(1, max(abs(self.x), abs(self.y))):
                deltas.append(direction * deltaMagnitude)
        else:
            raise NotImplementedError("Walks are only defined in the diagonals and orthoganals.")
        return deltas

    def clone(self) -> Vector:
        return Vector(self.x, self.y)


@dataclass
class UnfinishedVector():
    x: Optional[int]
    y: Optional[int]

    def toAN(self) -> str:
        return self.toAlgebreicNotation()

    def toAlgebreicNotation(self) -> str:
        sourceRank = chr(self.x+97) if not self.x is None else ""
        sourceFile = str(self.y+1) if not self.y is None else ""
        return sourceRank + sourceFile

class ANParsingError(ValueError):
    def __init__(self, ANText: str, errorMessage: str):
        super().__init__("Error trying to parse AN \"%s\": %s" % (ANText, errorMessage))