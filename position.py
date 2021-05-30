from __future__ import annotations
import random 
from typing import Iterable, List, Optional
from vector import Vector
from move import Move
from castling_move import CastlingMove
from dataclasses import dataclass, replace


class Position():
    def __init__(
            self, 
            _squares: List[List[str]] = None, 
            isWhiteToMove: bool = None, 
            castlingRights: CastlingRights = None, 
            enPassantPawn: Optional[Vector] = None, 
            halfClock: int = None,
            fullClock: int = None):
        self._squares = _squares or [["-" for x in range(8)] for y in range(8)]
        self.isWhiteToMove = isWhiteToMove or True
        self.castlingRights = castlingRights or CastlingRights()
        self.enPassantPawn = enPassantPawn or None
        self.halfClock = halfClock or 0
        self.fullClock = fullClock or 1
    
    def clone(self) -> Position:
        return Position(
            [[self._squares[y][x] for x in range(8)] for y in range(8)],
            self.isWhiteToMove,
            replace(self.castlingRights),
            self.enPassantPawn.clone() if self.enPassantPawn else None,
            self.halfClock,
            self.fullClock
        )

    def setPiece(self, vector: Vector, pieceType: str) -> Position:
        assert(vector.isInsideChessboard())
        if vector.y is None or vector.x is None: raise ValueError() #TODO: SMELL - Lazy Error Writing
        self._squares[vector.y][vector.x] = pieceType
        return self

    def pieceAt(self, vector: Vector) -> str:
        if (not vector.isInsideChessboard() or
            vector.y is None or 
            vector.x is None): 
                raise ValueError(vector) #TODO: SMELL - Lazy Error Writing
        return self._squares[vector.y][vector.x]

    def isEmptyAt(self, vector: Vector) -> bool:
        if not vector.isInsideChessboard():
            raise ValueError
        return self.pieceAt(vector) == "-"

    def pieceIsWhite(self, vector: Vector) -> bool:
        return self.pieceAt(vector).isupper()

    def pieceTypeOf(self, vector: Vector) -> str:
        return self.pieceAt(vector).upper()

    def pieceTypeIs(self, vector: Vector, pieceType: str) -> bool:
        return self.pieceAt(vector).upper() == pieceType.upper()

    def castle(self, move: CastlingMove) -> Position:
        return self.halfCastle(move).finishCastle(move)
    
    def halfCastle(self, move: CastlingMove) -> Position:
        clone = self.clone()
        if move.source is None: raise ValueError() #TODO: SMELL - Lazy Error Writing
        clone.setPiece(move.midStep(), self.pieceAt(move.source))
        clone.setPiece(move.source, "-")
        return clone
    
    def finishCastle(self, move: CastlingMove) -> Position:
        clone = self.clone()
        if move.source is None or move.destination is None or move.rookLocation is None: 
            raise ValueError() #TODO: SMELL - Lazy Error Writing
        clone.setPiece(move.destination, self.pieceAt(move.midStep()))
        clone.setPiece(move.midStep(), self.pieceAt(move.rookLocation))
        clone.setPiece(move.rookLocation, "-")
        clone.isWhiteToMove = not self.isWhiteToMove
        clone.enPassantPawn = None
        clone.halfClock = self.halfClock + 1 
        clone.fullClock = self.fullClock + (0 if self.isWhiteToMove else 1)
        return clone
    
    def next(self, move: Move) -> Position:
        if move.source is None or move.destination is None: raise ValueError() #TODO: SMELL - Lazy Error Writing
        source = move.source
        destination = move.destination
        clone = self.clone()
        clone.setPiece(destination, self.pieceAt(source))
        clone.setPiece(source, "-")
        clone.isWhiteToMove = not self.isWhiteToMove
        if destination.y is None or source.y is None: raise ValueError #TODO: SMELL - Lazy Error Writing
        clone.enPassantPawn = destination if move.pieceType == "P" and abs(destination.y - source.y) == 2 else None
        clone.halfClock = (self.halfClock + 1) if not move.isCapture else 0
        clone.fullClock = self.fullClock + (0 if self.isWhiteToMove else 1)
        return clone
    
    def findAll(self, pieceType: str) -> Iterable[Vector]:
        result = []
        for y, row in enumerate(self._squares):
            for x, currentPiece in enumerate(row):
                if currentPiece == pieceType:
                    result.append(Vector(x,y))
        return result
    
    def printBoard(self) -> None:
        for rankIndex in range(len(self._squares)-1,-1,-1):
            rank = self._squares[rankIndex]
            for piece in rank:
                print(piece, end=" ")
            print("")

    def getOrthogonalsTargeting(self, target: Vector) -> List[Vector]:
        xLine = [Vector(target.x, y) for y in range(0,8) if y != target.y]
        yLine = [Vector(x, target.y) for x in range(0,8) if x != target.x]
        orthogonals = xLine + yLine
        return orthogonals
    
    def getDiagonalsTargeting(self, target: Vector) -> List[Vector]:
        posPos = [target.plus( i, i) for i in range(1,8) if (target.plus( i, i)).isInsideChessboard()]
        posNeg = [target.plus(-i, i) for i in range(1,8) if (target.plus(-i, i)).isInsideChessboard()]
        NegPos = [target.plus( i,-i) for i in range(1,8) if (target.plus( i,-i)).isInsideChessboard()]
        NegNeg = [target.plus(-i,-i) for i in range(1,8) if (target.plus(-i,-i)).isInsideChessboard()]
        diagonals = posPos + posNeg + NegPos + NegNeg
        return diagonals
    
    def getKnightSquaresTargeting(self, target: Vector) -> List[Vector]:
        knightSquares = [target + deltaN for deltaN in [
            Vector( 1 , 2),
            Vector(-1 , 2),
            Vector( 1 ,-2),
            Vector(-1 ,-2),
            Vector( 2 , 1),
            Vector(-2 , 1),
            Vector( 2 ,-1),
            Vector(-2 ,-1)
        ] if (target + deltaN).isInsideChessboard()]
        return knightSquares
    
    def getWhitePawnsTargeting(self, target: Vector) -> List[Vector]:
        return [target + delta for delta in [Vector(1,-1), Vector(-1,-1)] if (target + delta).isInsideChessboard()]
    
    def getBlackPawnsTargeting(self, target: Vector):
        return [target + delta for delta in [Vector(1, 1), Vector(-1, 1)] if (target + delta).isInsideChessboard()]

    def getKingsTargeting(self, target:Vector):
        kingSquares = [target + deltaN for deltaN in [
            Vector(-1, 1), Vector(0, 1), Vector(1, 1),
            Vector(-1, 0), Vector(1, 0),
            Vector(-1,-1), Vector(0,-1), Vector(1,-1)
        ] if (target + deltaN).isInsideChessboard()]
        return kingSquares


@dataclass
class CastlingRights():
    whiteKingSide: bool = True
    whiteQueenSide: bool = True
    blackKingSide: bool = True
    blackQueenSide: bool = True
    
    @classmethod
    def fromFEN(cls, string: str) -> CastlingRights:
        return cls(
            "K" in string,
            "Q" in string,
            "k" in string,
            "q" in string
        )