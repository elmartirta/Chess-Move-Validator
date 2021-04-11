import random 
import re
from enum import Enum
from vector import Vector

class Position():
    def __init__(self, boardState=None, gameStatus=None, castlingRights=None, enPassantPawn=None, halfClock=None, fullClock=None):
        self.boardState = boardState or BoardState.fromEmpty()
        self.gameStatus = gameStatus or GameStatus.WHITE_TO_MOVE
        self.castlingRights = castlingRights or CastlingRights.fromAllTrue()
        self.enPassantPawn = enPassantPawn or Vector.fromNonExistent()
        self.halfClock = halfClock or 0
        self.fullClock = fullClock or 1
    def clone(self):
        return Position(
            self.boardState.clone(),
            self.gameStatus,
            self.castlingRights.clone(),
            self.enPassantPawn.clone(),
            self.halfClock,
            self.fullClock
        )

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
                    pos.boardState.addPiece(Vector(pieceIndex, 8-(rowIndex+1)),char)
                    pieceIndex += 1
                else:
                    raise FENParsingError(string, "Invalid character \"%s\" when parsing boardstate." % char)

        pos.gameStatus = GameStatus.WHITE_TO_MOVE if activeColorField == "w" else GameStatus.BLACK_TO_MOVE
        pos.castlingRights = CastlingRights.fromFEN(castlingRightsField)
        pos.enPassantPawn = Vector.fromAN(enPassantField) if enPassantField != "-" else Vector.fromNonExistent()
        pos.halfClock = int(halfClockField) 
        pos.fullMove = int(fullMoveField)
        return pos
    def fromStartingPosition():
        return Position.fromFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    def pieceAt(self, vector):
        if not vector.isInsideChessboard(): 
            raise ValueError(vector)
        return self.boardState.squares[vector.y][vector.x]
    def pieceIsWhite(self, vector):
        return self.pieceAt(vector).isupper()
    def pieceTypeOf(self, vector):
        return self.pieceAt(vector).upper()
    def isWhiteToMove(self):
        return self.gameStatus == GameStatus.WHITE_TO_MOVE
    def next(self, move):
        source = move.source
        destination = move.destination
        clone = self.clone()
        clone.boardState.squares[destination.y][destination.x] = self.boardState.squares[source.y][source.x]
        clone.boardState.squares[source.y][source.x] = "-"
        clone.gameStatus = GameStatus.WHITE_TO_MOVE if self.gameStatus == GameStatus.BLACK_TO_MOVE else GameStatus.BLACK_TO_MOVE
        clone.enPassantPawn = move.destination if (move.pieceType == "P" and abs(move.destination.y - move.source.y) == 2) else Vector.fromNonExistent()
        clone.halfClock = self.halfClock + 1 if (not move.isCapture) else 0
        clone.fullClock = self.fullClock + 1 if self.gameStatus == GameStatus.BLACK_TO_MOVE else self.fullClock
        return clone
class FENParsingError(ValueError):
    def __init__(self, FENString, message):
        super().__init__("\n\nError: The FEN string %s cannot be parsed:\n\t%s" %(FENString, message))

class BoardState():
    def __init__(self):
        self.squares = [["-" for x in range(8)] for y in range(8)]
    def clone(self):
        bs = BoardState()
        bs.squares = [[self.squares[y][x] for x in range(8)] for y in range(8)] 
        return bs
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
    def clone(self):
        return CastlingRights(
            self.whiteKingSide,
            self.whiteQueenSide,
            self.blackKingSide,
            self.blackQueenSide
        )
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