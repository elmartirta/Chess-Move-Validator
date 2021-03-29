from enum import Enum;
class Position():
    def init(self, boardState=None, gameStatus=None, castlingRights=None, enPassantPawn=None):
        self.boardState = boardState or emptyBoardState();
        self.gameStatus = gameStatus or emptyGameStatus();
        self.castlingRights = castlingRights or emptyCastlingRights();
        self.enPassantPawn = enPassantPawn or emptyEnpassantPawn();
    def emptyBoardState():
        self.boardState = BoardState.fromEmpty();
    def emptyGameStatus():
        self.gameStatus = GameStatus.WHITE_TO_MOVE;
    def emptyCastlingRights():
        self.castlingRights = CastlingRights.fromAllTrue();
    def emptyEnpassantPawn():
        self.enPassantPawn = CartesianCoordinate.NONEXISTANT;
    def addPiecesFromList(ANList):
        pos = Position()
        for pieceLocation in ANList:
            pieceType = pieceLocation[0]
            location = pieceLocation[1]
            board.addPiece.(Coord.fromAN(location), pieceType)))
        return pos
    def fromStartingPosition():
        pos = Position.fromEmpty();
        return Position.addPiecesFromList([
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
        ]);


class BoardState():
    def __init__(self):
        self.squares = [[Square(x,y) for x in range(8)]] for y in range(8)]
    def addPiece(self, coordinate, piece):
        self.squares[x,y].piece = piece;
        
class Square():
    def __init__(self,x,y,piece=None)
        self.coordinate = Coordinate(x,y);
        self.piece = piece;

class GameStatus(enum):
    WHITE_TO_MOVE = 1;
    BLACK_TO_MOVE = 2;
    WHITE_IN_MATE = 3;
    BLACK_IN_MATE = 4;
    STALEMATE = 5;

class CastlingRights():
    def __init__(self, blackKingSide=True,blackQueenSide=True,whiteKingSide=True,whiteQueenSide=True):
        self.blackKingSide = blackKingSide;
        self.blackQueenSide = blackQueenSide;
        self.whiteKingSide = whiteKingSide;
        self.whiteQueenSide = whiteQueenSide;
    def fromAllTrue():
        return CastlingRights();

class CartesianCoordinate():
    NONEXISTANT = Square(-1,-1);
    def __init__(self, x, y):
        self.x = x;
        self.y = y;
    def fromAN(string):
        self.x = string[0] - 94;
        self.y = string[1] - 1;


