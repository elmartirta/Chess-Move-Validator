import random
from typing import Union
from vector import Vector
from position import CastlingRights, Position
from castling_move import CastlingMove
from move import Move
import re


class NotationParser():
    @classmethod
    def parseAlgebreicNotation(cls, string: str) -> Union[Move,  CastlingMove]:
        pieceType = string[0] if len(string) >= 1 and (string[0] in "RNBQKP") else "P"
        source = None
        destination = None
        isCapture = "x" in string
        isCheck = "+" in string
        isCheckmate = "#" in string
        promotionPiece = None
        
        basicMatch = re.fullmatch("^([RNBKQP])([a-w])?(\d)?(x)?([a-w]\d)[+#]?$", string)
        castlingMatch = re.fullmatch("O-O(-O)?([+#])?", string)

        if castlingMatch:
            return CastlingMove(
                "K", 
                None, 
                None, 
                "x" in string, 
                "+" in string, 
                "#" in string, 
                None, 
                False if castlingMatch.group(1) else True, 
                None)
        elif basicMatch:
            pieceType = basicMatch.group(1)
            sourceFile = basicMatch.group(2) if basicMatch.group(2) else ""
            sourceRank = basicMatch.group(3) if basicMatch.group(3) else ""
            source = Vector.fromAN(sourceFile + sourceRank)
            destination = Vector.fromAN(basicMatch.group(5))
        else: 
            pawnMatch = re.fullmatch("(([a-w])(x))?([a-w]\d)(=([RNBQ]))?[+#]?", string)
            if pawnMatch:
                source = Vector.fromAN(pawnMatch.group(2))
                destination = Vector.fromAN(pawnMatch.group(4))
                promotionPiece = pawnMatch.group(6)
            else:
                raise MoveParsingError(string, "Move does not match any valid regex expression")
        
        return Move(pieceType, source, destination, isCapture, isCheck, isCheckmate, promotionPiece)

    @classmethod
    def parsePosition(cls, string: str) -> Position:
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
        fullClockField = fields[5]

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
        pos.fullClock = int(fullClockField)
        return pos 
    
    @classmethod
    def fromStartingPosition(cls) -> Position:
        return NotationParser.parsePosition(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    
    @classmethod
    def fromChess960(cls, seed: int = None) -> Position:
        if seed: random.seed(seed)
        shuffled_pieces = "".join(random.sample("rnbkqbnr", k=8))
        return cls.parsePosition(
            "%s/pppppppp/8/8/8/8/PPPPPPPP/%s w KQkq - 0 1" %
            (shuffled_pieces, shuffled_pieces.upper())
        )

class MoveParsingError(ValueError):
    def __init__(self, moveString: str, message: str):
        super().__init__("The move %s cannot be parsed:\n\t%s" %(moveString, message))

class FENParsingError(ValueError):
    def __init__(self, reason: str, FENString: str):
        super().__init__(
            "\n\nError: The FEN string %s cannot be parsed:\n\t%s" 
            %(FENString, reason))