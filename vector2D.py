#TODO: Un-object-orientify this Cartesian Vector class,
# so that this class is passed x, and y values, and simply returns them,
# instead of maintaining an internal state of x, and y.
# Perhaps rename it to some sort of custom math or coordinate class.

class Vector2D():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        if not isinstance(other, Vector2D): return False
        return Vector2D(self.x + other.x, self.y + other.y)
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
    def __sub__(self, other):
        if not isinstance(other, Vector2D): return False
        return Vector2D(self.x - other.x, self.y - other.y)
    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)
    def __rmul__(self, scalar):
        return (self * scalar)
    def __eq__(self, other):
        if not isinstance(other, Vector2D): return False
        return self.x == other.x and self.y == other.y
    def __repr__(self):
        return "Vector2D(%s, %s)" % (str(self.x), str(self.y))
    def fromAN(text):
        return Vector2D.fromAlgebreicNotation(text)
    def fromAlgebreicNotation(text):
        if (len(text) != 2): raise ANParsingError(text, "Length of text not equal to 2.")
        return Vector2D(ord(text[0].lower()) - 97, int(text[1])-1)
    def toAN(self):
        return self.toAlgebreicNotation()
    def toAlgebreicNotation(self):
        return chr(self.x+97)+str(self.y+1)
    def fromNonExistent():
        return Vector2D(None, None)
    def plus(self, other):
        return self + other
    def minus(self, other):
        return self - other
    def equals(self, other):
        return self == other
    def times(self, scalar):
        return self * scalar
    def toString(self):
        return str(self)
    def isInsideChessboard(self):
        return self.x >= 0 and self.x <= 7 and self.y >= 0 and self.y <= 7
    def getWalk(self):
        deltas = []
        direction = Vector2D(
            ((1 if self.x > 0 else -1) if self.x != 0 else 0),
            ((1 if self.y > 0 else -1) if self.y != 0 else 0)
        )
        for deltaMagnitude in range(1, max(abs(self.x), abs(self.y))):
            deltas.append(direction * deltaMagnitude)
        return deltas
class ANParsingError(ValueError):
    def __init__(self, ANText, errorMessage):
        super().__init__("Error trying to parse AN \"%s\": %s" % (ANText, errorMessage))