from __future__ import annotations
from typing import Iterable, Optional


class Vector():
    def __init__(self, x: Optional[int], y: Optional[int]):
        self.x = x
        self.y = y

    def __add__(self, other) -> Vector:
        if not isinstance(other, Vector): 
            raise TypeError(
                "Vector addition must use vectors, not %s and %s"
                 % (str(self), str(other)))
        if self.x is None or self.y is None or other.x is None or other.y is None: #TODO: SMELL - Repeated Code
            raise ValueError("Cannot add vectors that contain missing values")
        return Vector(self.x + other.x, self.y + other.y)

    def __radd__(self, other) -> Vector:
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__(self, other) -> Vector:
        if not isinstance(other, Vector):
             raise TypeError("Vector subtraction must use vectors")
        if self.x is None or self.y is None or other.x is None or other.y is None: #TODO: SMELL - Repeated Code
            raise ValueError("Cannot subtract vectors that contain missing values")     
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar) -> Vector:
        if not isinstance(scalar, int):
            raise TypeError("Vector scalar multiplication must use an int")
        if self.x is None or self.y is None: #TODO: SMELL - Repeated Code
            raise ValueError("Cannot perform scalar multiplication on vectors that contain missing values") 
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar) -> Vector:
        return (self * scalar)

    def __eq__(self, other) -> bool:
        if self is None or other is None: return False
        if not isinstance(other, Vector): 
            raise TypeError("Vector equality must use vectors")
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return "Vector(%s, %s)" % (str(self.x), str(self.y))

    @classmethod
    def fromAN(cls, text) -> Vector:
        return cls.fromAlgebreicNotation(text)

    @classmethod
    def fromAlgebreicNotation(cls, text) -> Vector:
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

    def plus(self, x, y) -> Vector:
        if self.x is None or self.y is None:
            raise ValueError("Missing Value in vector"+self.toString()) #TODO: SMELL - Repeated Code
        return Vector(self.x + x, self.y + y)

    def minus(self, x, y) -> Vector:
        if self.x is None or self.y is None:
            raise ValueError("Missing Value in vector"+self.toString()) #TODO: SMELL - Repeated Code
        return Vector(self.x - x, self.y - y) 

    def equals(self, x, y) -> bool:
        if self.x is None or self.y is None:
            raise ValueError("Missing Value in vector"+self.toString()) #TODO: SMELL - Repeated Code
        return self == Vector(x,y)

    def times(self, scalar) -> Vector:
        if self.x is None or self.y is None:
            raise ValueError("Missing Value in vector"+self.toString()) #TODO: SMELL - Repeated Code
        return self * scalar

    def toString(self) -> str:
        return str(self)

    def isInsideChessboard(self) -> bool:
        if self.x is None or self.y is None:
            raise ValueError("Missing Value in vector"+self.toString()) #TODO: SMELL - Repeated Code
        return self.x >= 0 and self.x <= 7 and self.y >= 0 and self.y <= 7

    def between(self, other) -> Iterable[Vector]:
        if self.x is None or self.y is None:
            raise ValueError("Missing Value in vector"+self.toString()) #TODO: SMELL - Repeated Code
        return [self + delta for delta in (other - self).walk()]

    def walk(self) -> Iterable[Vector]:
        if self.x is None or self.y is None:
            raise ValueError("Missing Value in vector"+self.toString()) #TODO: SMELL - Repeated Code
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
    def __init__(self, ANText, errorMessage):
        super().__init__("Error trying to parse AN \"%s\": %s" % (ANText, errorMessage))
