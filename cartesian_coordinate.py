#TODO: Un-object-orientify this Cartesian Coordinate class,
# so that this class is passed x, and y values, and simply returns them,
# instead of maintaining an internal state of x, and y.
# Perhaps rename it to some sort of custom math or coordinate class.

class CartesianCoordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)
    def __repr__(self):
        return "CartesianCoordinate(%s, %s)" % (str(self.x), str(self.y))
    def fromAN(text):
        return CartesianCoordinate.fromAlgebreicNotation(text)
    def fromAlgebreicNotation(text):
        if (len(text) != 2): raise ANParsingError(text, "Length of text not equal to 2.")
        return CartesianCoordinate.fromZeroZeroOrigin(ord(text[0].lower()) - 97, int(text[1])-1)
    def fromZeroZeroOrigin(x, y):
        return CartesianCoordinate(x, y)
    def fromOneOneOrigin(x, y):
        return CartesianCoordinate(x-1,y-1)
    def fromNonExistent():
        return CartesianCoordinate(None, None)
    def plus(self, x, y):
        return CartesianCoordinate(x+self.x, y+self.y)

class ANParsingError(ValueError):
    def __init__(self, ANText, errorMessage):
        super().__init__("Error trying to parse AN \"%s\": %s" % (ANText, errorMessage))
