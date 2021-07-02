from __future__ import annotations
from dataclasses import dataclass
from typing import List
from .vector import Vector

@dataclass
class Board():
    def __init__(self, squares: List[List[str]] = None):
        self._squares = squares or [["-" for _ in range(8)] for _ in range(8)]

    @staticmethod
    def fromFEN(fenString: str) -> Board:
        board = Board()
        rows = fenString.split("/")
        for rowIndex in range(0, len(rows)):
            row = rows[rowIndex]
            pieceIndex = 0
            for char in row:
                if pieceIndex >= 8: 
                    break
                if char.isdigit():
                    pieceIndex += int(char)
                elif char.isalpha():
                    board.setPiece(Vector(pieceIndex, 8-(rowIndex+1)),char)
                    pieceIndex += 1
                else:
                    raise ValueError(
                        "Invalid character \"%s\" when parsing boardstate. %s" 
                    % (char, fenString))
        return board

    def clone(self) -> Board:
        board = Board()
        board._squares = [[self._squares[y][x] for x in range(8)] for y in range(8)]
        return board

    def setPiece(self, vector: Vector, pieceType: str) -> Board:
        assert(vector.isInsideChessboard())
        self._squares[vector.y][vector.x] = pieceType
        return self

    def pieceAt(self, vector: Vector) -> str:
        if (not vector.isInsideChessboard()): 
            raise ValueError(vector)
        return self._squares[vector.y][vector.x]

    def isEmptyAt(self, vector: Vector) -> bool:
        if not vector.isInsideChessboard():
            raise ValueError
        return self.pieceAt(vector) == "-"

    def pieceCanSee(self, attacker: Vector, target: Vector) -> bool:
        return all([self.isEmptyAt(s) for s in attacker.between(target)])

    def pieceIsWhite(self, vector: Vector) -> bool:
        return self.pieceAt(vector).isupper()

    def pieceTypeOf(self, vector: Vector) -> str:
        return self.pieceAt(vector).upper()

    def pieceTypeIs(self, vector: Vector, pieceType: str) -> bool:
        return self.pieceAt(vector).upper() == pieceType.upper()

    def findAll(self, pieceType: str) -> List[Vector]:
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
    
    def getBlackPawnsTargeting(self, target: Vector) -> List[Vector]:
        return [target + delta for delta in [Vector(1, 1), Vector(-1, 1)] if (target + delta).isInsideChessboard()]

    def getKingsTargeting(self, target:Vector) -> List[Vector]:
        kingSquares = [target + deltaN for deltaN in [
            Vector(-1, 1), Vector(0, 1), Vector(1, 1),
            Vector(-1, 0), Vector(1, 0),
            Vector(-1,-1), Vector(0,-1), Vector(1,-1)
        ] if (target + deltaN).isInsideChessboard()]
        return kingSquares
    
    def getRooksAttacking(self, target: Vector): 
        return list(filter(
            lambda v: self.pieceTypeIs(v, "R"), 
            self.getOrthogonalsTargeting(target)))

    def getBishopsAttacking(self, target: Vector): 
        return list(filter(
            lambda v: self.pieceTypeIs(v, "B"), 
            self.getDiagonalsTargeting(target)))

    def getQueensAttacking(self, target: Vector): 
        return list(filter(
            lambda v: self.pieceTypeIs(v, "Q"), 
            self.getOrthogonalsTargeting(target) + self.getDiagonalsTargeting(target)))
    
    def getKnightsAttacking(self, target: Vector):
        return list(filter(
            lambda v: self.pieceTypeIs(v, "N"), 
            self.getKnightSquaresTargeting(target)))
    
    def getPawnsAttacking(self, target:Vector):
        whites = list(filter(lambda p: self.pieceIsWhite(p), self.getWhitePawnsTargeting(target)))
        blacks = list(filter(lambda p: not self.pieceIsWhite(p), self.getBlackPawnsTargeting(target)))
        return list(filter(
            lambda v: self.pieceTypeIs(v, "P"),
            whites + blacks
        ))
    
    def getPawnsWalkingTo(self, target:Vector):
        whites = [target.plus(0,-1), target.plus(0, -2)] if target.y == 3 else [target.plus(0,-1)]
        blacks = [target.plus(0, 1), target.plus(0,  2)] if target.y == 4 else [target.plus(0, 1)]
        whites = list(filter(lambda p: p.isInsideChessboard(), whites))
        blacks = list(filter(lambda p: p.isInsideChessboard(), blacks))
        whites = list(filter(lambda p: self.pieceIsWhite(p), whites))
        blacks = list(filter(lambda p: not self.pieceIsWhite(p), blacks))
        return list(filter(
            lambda v: self.pieceTypeIs(v, "P"),
            whites + blacks
        ))