from __future__ import annotations
from typing import List, Optional


class Vector():
    def __init__(self, x: Optional[int], y: Optional[int]):
        # TODO: SMELL - MAJOR CODE SMELL - The issue with Vector being constructed using 
        # Optional[int]s,is that it casts doubt throughout the entire codebase, whether a vector 
        # you're using, actually has information. It's the source of many, many, many null checks, 
        # (especially since mypy is particularly strict about adding potential None values
        # together). However, "Unfinished" vectors do have a place in this codebase. The move
        # Rbd1, for instance, has the source vector "b", with no information about the other
        # value. Therefore, a potential solution would be to this functionality into a
        # "Finished" and "Unfinished" vector class, where the Unfinished vector class
        # has Optional[int] values, and where the Vector class, must have filled in int values.
        # That way, the logic of filling in values, and using them,can be separated into two 
        # different areas. 
        # 
        # - Elmar, May 2021

        self.x = x
        self.y = y

    def __add__(self, other: Vector) -> Vector:
        if (self.x is None or 
            self.y is None or 
            other.x is None or 
            other.y is None):
            raise ValueError(
                "Cannot add vectors that contain missing values"
            )#TODO : SMELL - Repeated Code
        return Vector(self.x + other.x, self.y + other.y)

    def __radd__(self, other: Vector) -> Vector:
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__(self, other: Vector) -> Vector:
        if (self.x is None or 
            self.y is None or 
            other.x is None or 
            other.y is None):
            raise ValueError(
                "Cannot subtract vectors that contain missing values"
            )#TODO : SMELL - Repeated Code
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: int) -> Vector:
        if (self.x is None or 
            self.y is None):
            raise ValueError(
                "Cannot perform scalar multiplication on vectors that contain missing values"
            ) #TODO : SMELL - Repeated Code
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
    def fromAN(cls, text: str) -> Vector:
        return cls.fromAlgebreicNotation(text)

    @classmethod
    def fromAlgebreicNotation(cls, text: str) -> Vector:
        toX = lambda chr : ord(chr.lower()) - 97
        toY = lambda chr : int(chr)-1
        if text is None or len(text) == 0:
            x,y = None, None
        elif len(text) == 1:
            if text[0].isalpha():
                x,y = toX(text[0]), None
            else:
                x,y = None, toY(text[0])
        elif len(text) == 2:
            x,y = toX(text[0]), toY(text[1])
        else:
            raise ANParsingError(text, "Length of the text is longer than 2")
        return cls(x,y)

    def toAN(self) -> str:
        return self.toAlgebreicNotation()

    def toAlgebreicNotation(self) -> str:
        sourceRank = chr(self.x+97) if not self.x is None else ""
        sourceFile = str(self.y+1) if not self.y is None else ""
        return sourceRank + sourceFile

    def plus(self, x: int, y: int) -> Vector:
        if (self.x is None or 
            self.y is None):
            raise ValueError(
                "Missing Value in vector"+self.toString()
            )#TODO : SMELL - Repeated Code
        return Vector(self.x + x, self.y + y)

    def minus(self, x: int, y: int) -> Vector:
        if (self.x is None or 
            self.y is None):
            raise ValueError(
                "Missing Value in vector"+self.toString()
            )#TODO : SMELL - Repeated Code
        return Vector(self.x - x, self.y - y) 

    def equals(self, x: int, y: int) -> bool:
        if (self.x is None or 
            self.y is None):
            raise ValueError(
                "Missing Value in vector"+self.toString()
            )#TODO : SMELL - Repeated Code
        return self == Vector(x,y)

    def times(self, scalar: int) -> Vector:
        if (self.x is None or 
            self.y is None):
            raise ValueError(
                "Missing Value in vector"+self.toString()
            )#TODO : SMELL - Repeated Code
        return self * scalar

    def toString(self) -> str:
        return str(self)

    def isInsideChessboard(self) -> bool:
        if (self.x is None or 
            self.y is None):
            raise ValueError(
                "Missing Value in vector"+self.toString()
            )#TODO : SMELL - Repeated Code
        return self.x >= 0 and self.x <= 7 and self.y >= 0 and self.y <= 7

    def between(self, other: Vector) -> List[Vector]:
        if (self.x is None or 
            self.y is None):
            raise ValueError(
                "Missing Value in vector"+self.toString()
            )#TODO : SMELL - Repeated Code
        return [self + delta for delta in (other - self).walk()]

    def walk(self) -> List[Vector]:
        if (self.x is None or 
            self.y is None):
            raise ValueError(
                "Missing Value in vector"+self.toString()
            ) #TODO: SMELL - Repeated Code
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

        
class ANParsingError(ValueError):
    def __init__(self, ANText: str, errorMessage: str):
        super().__init__("Error trying to parse AN \"%s\": %s" % (ANText, errorMessage))