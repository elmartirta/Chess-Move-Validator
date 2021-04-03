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
        return CartesianCoordinate(ord(text[0].lower()) - 96, int(text[1]))
    def fromNonExistent():
        return CartesianCoordinate(None, None)