import random 
import re
from enum import Enum
from vector2D import Vector2D

class Position():
    def __init__(self, boardState=None, gameStatus=None, castlingRights=None, enPassantPawn=None, halfClock=None, fullClock=None):
        self.boardState = boardState or BoardState.fromEmpty()
        self.gameStatus = gameStatus or GameStatus.WHITE_TO_MOVE
        self.castlingRights = castlingRights or CastlingRights.fromAllTrue()
        self.enPassantPawn = enPassantPawn or Vector2D.fromNonExistent()
        self.halfClock = halfClock or 0
        self.fullClock = fullClock or 1
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
        if (string == None): 
            raise FENParsingError(string, "String is equal to None")
        if (string == ""): 
            raise FENParsingError(string, "String is the empty String")
        if not re.fullmatch("([rnbqkpRNBQKP\d]{1,8}\/){7}[rnbqkpRNBQKP\d]{1,8} [wb] [KQkq-]{1,4} [a-h\-]\d* \d \d\d*", string):
            raise FENParsingError(string, "Forsyth Edwards Notation must be in the correct format")
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
                    pos.boardState.addPiece(Vector2D(pieceIndex, 8-(rowIndex+1)),char)
                    pieceIndex += 1
                else:
                    raise FENParsingError(string, "Invalid character \"%s\" when parsing boardstate." % char)

        pos.gameStatus = GameStatus.WHITE_TO_MOVE if activeColorField == "w" else GameStatus.BLACK_TO_MOVE
        pos.castlingRights = CastlingRights.fromFEN(castlingRightsField)
        pos.enPassantPawn = Vector2D.fromAN(enPassantField) if enPassantField != "-" else Vector2D.fromNonExistent()
        pos.halfClock = int(halfClockField) 
        pos.fullMove = int(fullMoveField)
        return pos
    def fromStartingPosition():
        return Position.fromFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    def pieceAt(self, vector):
        if not vector.isInsideChessboard(): 
            raise ValueError(vector)
        return self.boardState.squares[vector.y][vector.x]
class FENParsingError(ValueError):
    def __init__(self, FENString, message):
        super().__init__("\n\nError: The FEN string %s cannot be parsed:\n\t%s" %(FENString, message))

class BoardState():
    def __init__(self):
        self.squares = [["-" for x in range(8)] for y in range(8)]
    def fromEmpty():
        return BoardState()
    def addPiece(self, vector, piece):
        assert(vector.isInsideChessboard())
        self.squares[vector.y][vector.x] = piece
    def toString(self):
        for rankIndex in range(len(self.squares)-1,-1,-1):
            rank = self.squares[rankIndex]
            for piece in rank:
                print(piece, end=" ")
            print("")

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
    def __eq__(self, other):
        return \
            self.whiteKingSide == other.whiteKingSide and \
            self.whiteQueenSide == other.whiteQueenSide and \
            self.blackKingSide == other.blackKingSide and \
            self.blackQueenSide == other.blackQueenSide
    def fromAllTrue():
        return CastlingRights()
    def fromFEN(string):
        return CastlingRights(
            "K" in string,
            "Q" in string,
            "k" in string,
            "q" in string
        )