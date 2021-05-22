import random 
import re
from enum import Enum
from vector import Vector
from dataclasses import dataclass, replace

class Position():
    def __init__(
            self, 
            squares=None, 
            isWhiteToMove=None, 
            castlingRights=None, 
            enPassantPawn=None, 
            halfClock=None, 
            fullClock=None):
        self.squares = squares or [["-" for x in range(8)] for y in range(8)]
        self.isWhiteToMove = isWhiteToMove or True
        self.castlingRights = castlingRights or CastlingRights()
        self.enPassantPawn = enPassantPawn or None
        self.halfClock = halfClock or 0
        self.fullClock = fullClock or 1

    @staticmethod
    def fromChess960(seed=None):
        if seed: random.seed(seed)
        shuffled_pieces = "".join(random.sample("rnbkqbnr", k=8))
        return Position.fromFEN(
            "%s/pppppppp/8/8/8/8/PPPPPPPP/%s w KQkq - 0 1" %
            (shuffled_pieces, shuffled_pieces.upper())
        )

    @staticmethod
    def fromFEN(string):
        return Position.fromForsythEdwardsNotation(string)

    @staticmethod
    def fromForsythEdwardsNotation(string):
        if (string == None): 
            raise FENParsingError(
                    "String is equal to None",
                string) 
        if (string == ""): 
            raise FENParsingError(
                    "String is the empty String",
                string)
        fields = string.split(" ")
        if len(fields) != 6: 
            raise FENParsingError(
                    "\Forsyth-Edwards Notation must have 6 fields, separated by 6 spaces",
                string) 

        if not re.fullmatch("([rnbqkpRNBQKP\d]{1,8}\/){7}[rnbqkpRNBQKP\d]{1,8} [wb] [KQkq-]{1,4} [a-h\-]\d* \d \d\d*", string):
            raise FENParsingError(
                    "Forsyth Edwards Notation must be in the correct format",
                string) 
        
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
                    pos.setPiece(Vector(pieceIndex, 8-(rowIndex+1)),char)
                    pieceIndex += 1
                else:
                    raise FENParsingError(
                        "Invalid character \"%s\" when parsing boardstate." % char,
                        string) 

        pos.isWhiteToMove = True if activeColorField == "w" else False
        pos.castlingRights = CastlingRights.fromFEN(castlingRightsField)
        pos.enPassantPawn = Vector.fromAN(enPassantField) if enPassantField != "-" else None
        pos.halfClock = int(halfClockField) 
        pos.fullMove = int(fullMoveField)
        return pos

    @staticmethod
    def fromStartingPosition():
        return Position.fromFEN(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
            
    def clone(self):
        return Position(
            [[self.squares[y][x] for x in range(8)] for y in range(8)],
            self.isWhiteToMove,
            replace(self.castlingRights),
            self.enPassantPawn.clone() if self.enPassantPawn else None,
            self.halfClock,
            self.fullClock
        )


    def setPiece(self, vector, pieceType):
        assert(vector.isInsideChessboard())
        self.squares[vector.y][vector.x] = pieceType

    def pieceAt(self, vector):
        if not vector.isInsideChessboard(): 
            raise ValueError(vector)
        return self.squares[vector.y][vector.x]

    def isEmptyAt(self, vector):
        if not vector.isInsideChessboard():
            raise ValueError
        return self.pieceAt(vector) == "-"
    def pieceIsWhite(self, vector):
        return self.pieceAt(vector).isupper()

    def pieceTypeOf(self, vector):
        return self.pieceAt(vector).upper()

    def pieceTypeIs(self, vector, pieceType):
        return self.pieceAt(vector).upper() == pieceType.upper()

    def castle(self, move):
        return self.halfCastle(move).finishCastle(move)
    
    def halfCastle(self, move):
        clone = self.clone()
        clone.setPiece(move.midStep(), self.pieceAt(move.source))
        clone.setPiece(move.source, "-")
        return clone
    
    def finishCastle(self, move):
        clone = self.clone()
        clone.setPiece(move.destination, self.pieceAt(move.midStep()))
        clone.setPiece(move.midStep(), self.pieceAt(move.rookLocation))
        clone.setPiece(move.rookLocation, "-")
        clone.isWhiteToMove = not self.isWhiteToMove
        clone.enPassantPawn = None
        clone.halfClock = self.halfClock + 1 
        clone.fullClock = self.fullClock + (0 if self.isWhiteToMove else 1)
        return clone
    
    def next(self, move):
        source = move.source
        destination = move.destination
        clone = self.clone()
        clone.setPiece(destination, self.pieceAt(source))
        clone.setPiece(source, "-")
        clone.isWhiteToMove = not self.isWhiteToMove
        clone.enPassantPawn = destination if move.pieceType == "P" and abs(destination.y - source.y) == 2 else None
        clone.halfClock = (self.halfClock + 1) if not move.isCapture else 0
        clone.fullClock = self.fullClock + (0 if self.isWhiteToMove else 1)
        return clone
    
    def findAll(self, pieceType):
        result = []
        for y, row in enumerate(self.squares):
            for x, currentPiece in enumerate(row):
                if currentPiece == pieceType:
                    result.append(Vector(x,y))
        return result
    
    def printBoard(self):
        for rankIndex in range(len(self.squares)-1,-1,-1):
            rank = self.squares[rankIndex]
            for piece in rank:
                print(piece, end=" ")
            print("")


class FENParsingError(ValueError):
    def __init__(self, reason, FENString):
        super().__init__(
            "\n\nError: The FEN string %s cannot be parsed:\n\t%s" 
            %(FENString, reason))

@dataclass
class CastlingRights():
    whiteKingSide: bool = True
    whiteQueenSide: bool = True
    blackKingSide: bool = True
    blackQueenSide: bool = True
    
    def fromFEN(string):
        return CastlingRights(
            "K" in string,
            "Q" in string,
            "k" in string,
            "q" in string
        )