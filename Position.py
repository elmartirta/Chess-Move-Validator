import random 
import re
from enum import Enum
from cartesian_coordinate import CartesianCoordinate

class Position():
    def __init__(self, boardState=None, gameStatus=None, castlingRights=None, enPassantPawn=None, halfClock=None, fullClock=None):
        self.boardState = boardState or Position.emptyBoardState()
        self.gameStatus = gameStatus or Position.emptyGameStatus()
        self.castlingRights = castlingRights or Position.emptyCastlingRights()
        self.enPassantPawn = enPassantPawn or Position.emptyEnpassantPawn()
        self.halfClock = halfClock or 0
        self.fullClock = fullClock or 1
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
        return self
    def fromStartingPosition():
        return Position.fromFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    def fromChess960(seed=None):
        if seed: random.seed(seed)
        shuffled_pieces = "".join(random.sample("rnbkqbnr", k=8))
        return Position.fromFEN(
            "%s/pppppppp/8/8/8/8/PPPPPPPP/%s w KQkq - 0 1" %
            (shuffled_pieces, shuffled_pieces.upper())
        )
    def fromFEN(string):
        return Position.fromForsythEdwardsNotation(string)
    def fromForsythEdwardsNotation(string):
        if not re.fullmatch("[\w]+\/[\w]+\/[\w]+\/[\w]+\/[\w]+\/[\w]+\/[\w]+\/[\w]+\s[\w]\s[\w-]+\s[\w-]+\s\d\s\d", string):
            raise FENParsingError(string, "Forsyth Edwards Notation must be in the format: \n\t[a#]/[a#]/[a#]/[a#]/[a#]/[a#]/[a#]/[a#] a a a # #")
        
        fields = string.split(" ")
        if len(fields) != 6: 
            raise FENParsingError(string, "\Forsyth-Edwards Notation must have 6 fields, separated by 6 spaces")
        pos = Position()
        piecePlacementField = fields[0]
        activeColorField = fields[1]
        castlingRightsField = fields[2]
        enPassantField = fields[3]
        halfClockField = fields[4]
        fullMoveField = fields[5]

        rows = piecePlacementField.split("/")
        for rowIndex in range(0, len(rows)):
            row = rows[rowIndex]
            pieceIndex = 0
            for char in row:
                if pieceIndex >= 8: 
                    break
                if char.isdigit():
                    pieceIndex += int(char)
                elif char.isalpha():
                    pos.boardState.addPiece(CartesianCoordinate(pieceIndex+1, rowIndex+1),char)
                    pieceIndex += 1
                else:
                    raise FENParsingError(string, "Invalid character \"%s\" when parsing boardstate." % char)

        pos.gameStatus = GameStatus.WHITE_TO_MOVE if activeColorField == "w" else GameStatus.BLACK_TO_MOVE
        pos.castlingRights = CastlingRights.fromFEN(castlingRightsField)
        pos.enPassantPawn = CartesianCoordinate.fromAN(enPassantField) if enPassantField != "-" else CartesianCoordinate.fromNonExistent()
        pos.halfClock = int(halfClockField) 
        pos.fullMove = int(fullMoveField)
        return pos

class FENParsingError(ValueError):
    def __init__(self, FENString, message):
        super().__init__("\n\nError: The FEN string %s cannot be parsed:\n\t%s" %(FENString, message))

class BoardState():
    def __init__(self):
        self.squares = [[Square(x,y) for x in range(8)] for y in range(8)]
    def addPiece(self, coordinate, piece):
        self.squares[coordinate.y-1][coordinate.x - 1].piece = piece
    def toString(self):
        for rankIndex in range(len(self.squares)-1,-1,-1):
            rank = self.squares[rankIndex]
            printedLine = ""
            for square in rank:
                printedLine += square.piece + " "
            print(printedLine)
                        
class Square():
    def __init__(self,x,y,piece=None):
        self.coordinate = CartesianCoordinate(x,y)
        self.piece = piece or "-"

class GameStatus(Enum):
    WHITE_TO_MOVE = 1
    BLACK_TO_MOVE = 2
    WHITE_IN_MATE = 3
    BLACK_IN_MATE = 4
    STALEMATE = 5

class CastlingRights():
    def __init__(self, whiteKingSide=True,whiteQueenSide=True,blackKingSide=True,blackQueenSide=True):
        self.whiteKingSide = whiteKingSide
        self.whiteQueenSide = whiteQueenSide
        self.blackKingSide = blackKingSide
        self.blackQueenSide = blackQueenSide
    def fromAllTrue():
        return CastlingRights()
    def fromFEN(string):
        return CastlingRights(
            "K" in string,
            "Q" in string,
            "k" in string,
            "q" in string
        )