from enum import Enum
class Position():
    def __init__(self, boardState=None, gameStatus=None, castlingRights=None, enPassantPawn=None):
        self.boardState = boardState or Position.emptyBoardState()
        self.gameStatus = gameStatus or Position.emptyGameStatus()
        self.castlingRights = castlingRights or Position.emptyCastlingRights()
        self.enPassantPawn = enPassantPawn or Position.emptyEnpassantPawn()
    def emptyBoardState():
        return BoardState()
    def emptyGameStatus():
        return GameStatus.WHITE_TO_MOVE
    def emptyCastlingRights():
        return CastlingRights.fromAllTrue()
    def emptyEnpassantPawn():
        return CartesianCoordinate.fromNonExistent()
    def addPiecesFromList(self, ANList):
        for pieceLocation in ANList:
            location = pieceLocation[0]
            pieceType = pieceLocation[1]
            self.boardState.addPiece(CartesianCoordinate.fromAN(location), pieceType)
    def fromStartingPosition():
        pos = Position()
        return pos.addPiecesFromList([
            ("a1","r"),
            ("b1","n"),
            ("c1","b"),
            ("d1","q"),
            ("e1","k"),
            ("f1","b"),
            ("g1","n"),
            ("h1","r"),

            ("a2", "p"),
            ("b2", "p"),
            ("c2", "p"),
            ("d2", "p"),
            ("e2", "p"),
            ("f2", "p"),
            ("g2", "p"),
            ("h2", "p"),
            
            ("a7", "p"),
            ("b7", "p"),
            ("c7", "p"),
            ("d7", "p"),
            ("e7", "p"),
            ("f7", "p"),
            ("g7", "p"),
            ("h7", "p"),
            
            ("a8","r"),
            ("b8","n"),
            ("c8","b"),
            ("d8","q"),
            ("e8","k"),
            ("f8","b"),
            ("g8","n"),
            ("h8","r")
        ])


class BoardState():
    def __init__(self):
        self.squares = [[Square(x,y) for x in range(8)] for y in range(8)]
    def addPiece(self, coordinate, piece):
        self.squares[coordinate.x - 1][coordinate.y - 1].piece = piece
        
class Square():
    def __init__(self,x,y,piece=None):
        self.coordinate = CartesianCoordinate(x,y)
        self.piece = piece

class GameStatus(Enum):
    WHITE_TO_MOVE = 1
    BLACK_TO_MOVE = 2
    WHITE_IN_MATE = 3
    BLACK_IN_MATE = 4
    STALEMATE = 5

class CastlingRights():
    def __init__(self, blackKingSide=True,blackQueenSide=True,whiteKingSide=True,whiteQueenSide=True):
        self.blackKingSide = blackKingSide
        self.blackQueenSide = blackQueenSide
        self.whiteKingSide = whiteKingSide
        self.whiteQueenSide = whiteQueenSide
    def fromAllTrue():
        return CastlingRights()

class CartesianCoordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def fromAN(text):
        return CartesianCoordinate.fromAlgebreicNotation(text)
    def fromAlgebreicNotation(text):
        return CartesianCoordinate(ord(text[0].lower()) - 96, int(text[1]) - 1)
    def fromNonExistent():
        return CartesianCoordinate(None, None)


