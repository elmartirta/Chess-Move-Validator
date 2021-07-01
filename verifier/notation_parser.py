from .board import Board
import random
from .vector import UnfinishedVector, Vector
from .position import CastlingRights, Position
from .castling_move import UnfinishedCastlingMove
from .move import UnfinishedMove
import re


class NotationParser():
    @classmethod
    def parseAlgebreicNotation(cls, string: str) -> UnfinishedMove:        
        basicMatch = re.fullmatch("^([RNBKQP])([a-h]?[1-8]?)x?([a-h][1-8])[+#]?$", string)
        castlingMatch = re.fullmatch("O-O(-O)?[+#]?", string)
        pawnMatch = re.fullmatch("(?:([a-h])x)?([a-h][1-8])(?:=([RNBQ]))?[+#]?", string)

        if castlingMatch:
            return UnfinishedCastlingMove(
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
            return UnfinishedMove(
                basicMatch.group(1), 
                Vector.fromAN(basicMatch.group(2)), 
                Vector.fromANStrict(basicMatch.group(3)), 
                "x" in string, 
                "+" in string, 
                "#" in string, 
                None)
        elif pawnMatch: 
            return UnfinishedMove(
                "P", 
                Vector.fromAN(pawnMatch.group(1)), 
                Vector.fromANStrict(pawnMatch.group(2)), 
                "x" in string, 
                "+" in string, 
                "#" in string, 
                pawnMatch.group(3))
        else:
            raise MoveParsingError(string, "Move does not match any valid regex expression")
        

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
        pos.board = Board.fromFEN(fields[0])
        pos.isWhiteToMove = fields[1] == "w"
        pos.castlingRights = CastlingRights.fromFEN(fields[2])
        pos.enPassantPawn = Vector.fromANStrict(fields[3]) if fields[3] != "-" else None
        pos.halfClock = int(fields[4]) 
        pos.fullClock = int(fields[5])
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
            f"{shuffled_pieces}/pppppppp/8/8/8/8/PPPPPPPP/{shuffled_pieces.upper()} w KQkq - 0 1"
        )

class MoveParsingError(ValueError):
    def __init__(self, moveString: str, message: str):
        super().__init__(f"The move {moveString} cannot be parsed:\n\t{message}")

class FENParsingError(ValueError):
    def __init__(self, reason: str, FENString: str):
        super().__init__(
            f"\n\nError: The FEN string {FENString} cannot be parsed:\n\t{reason}")