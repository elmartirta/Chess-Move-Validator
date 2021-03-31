class CartesianCoordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def fromAN(text):
        return CartesianCoordinate.fromAlgebreicNotation(text)
    def fromAlgebreicNotation(text):
        return CartesianCoordinate(ord(text[0].lower()) - 96, int(text[1]))
    def fromNonExistent():
        return CartesianCoordinate(None, None)