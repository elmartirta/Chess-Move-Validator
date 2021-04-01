from enum import Enum
from CartesianCoordinate import CartesianCoordinate
import re

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
        return self
    def fromStartingPosition():
        pos = Position()
        return pos.addPiecesFromList([
            ("a1","r"),
            ("b1","n"),
            ("c1","b"),
            ("d1","q"),
            ("e4","x"),
            ("e3","x"),
            ("e2","x"),
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
            
            ("a7", "P"),
            ("b7", "P"),
            ("c7", "P"),
            ("d7", "P"),
            ("e7", "P"),
            ("f7", "P"),
            ("g7", "P"),
            ("h7", "P"),
            
            ("a8","R"),
            ("b8","N"),
            ("c8","B"),
            ("d8","Q"),
            ("e8","K"),
            ("f8","B"),
            ("g8","N"),
            ("h8","R")
        ])
    
    def fromFEN(string):
        return Position.fromForsythEdwardsNotation(string)
    def fromForsythEdwardsNotation(string):
        if not re.fullmatch("[\w]+\/[\w]+\/[\w]+\/[\w]+\/[\w]+\/[\w]+\/[\w]+\/[\w]+\s[\w]\s[\w-]+\s[\w-]+\s\d\s\d", string):
            raise FENParsingError(string, "Forsyth Edwards Notation must be in the format: \n\t[a#]/[a#]/[a#]/[a#]/[a#]/[a#]/[a#]/[a#] a a a # #")
        
        fields = string.split(" ")
        if len(fields) != 6: 
            raise FENParsingError(string, "\Forsyth-Edwards Notation must have 6 fields, separated by 6 spaces")

        pos = Position()
        piecePlacement = fields[0]
        activeColor = fields[1]
        castling = fields[2]
        enPassant = fields[3]
        halfClock = fields[4]
        fullMove = fields[5]

        rows = piecePlacement.split("/")
        for rowIndex in range(0, len(rows)):
            row = rows[rowIndex]
            
            pieceIndex = 0
            charIndex = 0
            while(pieceIndex < 8 and charIndex < len(row)):
                currentChar = row[charIndex]
                if currentChar.isalpha():
                    pos.boardState.addPiece(CartesianCoordinate(pieceIndex+1, rowIndex+1), currentChar)
                    pieceIndex += 1
                    charIndex += 1
                elif currentChar.isdigit():
                    pieceIndex += int(currentChar)
                    charIndex += 1
                else:
                    raise FENParsingError(string, "Invalid character \"%s\" when parsing boardstate." % currentChar)

        print(fields)
        print(pos.boardState.toString())
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
    def __init__(self, blackKingSide=True,blackQueenSide=True,whiteKingSide=True,whiteQueenSide=True):
        self.blackKingSide = blackKingSide
        self.blackQueenSide = blackQueenSide
        self.whiteKingSide = whiteKingSide
        self.whiteQueenSide = whiteQueenSide
    def fromAllTrue():
        return CastlingRights()




