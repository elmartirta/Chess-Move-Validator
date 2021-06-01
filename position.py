from __future__ import annotations
from typing import Optional
from vector import UnfinishedVector, Vector
from board import Board
from move import Move
from castling_move import CastlingMove
from dataclasses import dataclass, replace


class Position():
    def __init__(
            self,
            board: Board = None,
            isWhiteToMove: bool = None, 
            castlingRights: CastlingRights = None, 
            enPassantPawn: Optional[Vector] = None, 
            halfClock: int = None,
            fullClock: int = None):
        self.board = board or Board()
        self.isWhiteToMove = isWhiteToMove or True
        self.castlingRights = castlingRights or CastlingRights()
        self.enPassantPawn = enPassantPawn or None
        self.halfClock = halfClock or 0
        self.fullClock = fullClock or 1
    
    def clone(self) -> Position:
        return Position(
            self.board.clone(),
            self.isWhiteToMove,
            replace(self.castlingRights),
            self.enPassantPawn.clone() if self.enPassantPawn else None,
            self.halfClock,
            self.fullClock
        )
    
    def castle(self, move: CastlingMove) -> Position:
        return self.halfCastle(move).finishCastle(move)
    
    def halfCastle(self, move: CastlingMove) -> Position:
        if (move.source is None or
            isinstance(move.source, UnfinishedVector)): raise ValueError() #TODO: SMELL - Lazy Error Writing
        clone = self.clone()
        clone.board.setPiece(move.midStep(), self.board.pieceAt(move.source))
        clone.board.setPiece(move.source, "-")
        return clone
    
    def finishCastle(self, move: CastlingMove) -> Position:
        clone = self.clone()
        if (move.source is None or 
                move.destination is None or 
                move.rookLocation is None or
                isinstance(move.source, UnfinishedVector) or
                isinstance(move.destination, UnfinishedVector)): 
            raise ValueError() #TODO: SMELL - Lazy Error Writing
        clone.board.setPiece(move.destination, self.board.pieceAt(move.midStep()))
        clone.board.setPiece(move.midStep(), self.board.pieceAt(move.rookLocation))
        clone.board.setPiece(move.rookLocation, "-")
        clone.isWhiteToMove = not self.isWhiteToMove
        clone.enPassantPawn = None
        clone.halfClock = self.halfClock + 1 
        clone.fullClock = self.fullClock + (0 if self.isWhiteToMove else 1)
        return clone
    
    def next(self, move: Move) -> Position:
        if (move.source is None or 
                move.destination is None or 
                isinstance(move.source, UnfinishedVector) or
                isinstance(move.destination, UnfinishedVector)): 
            raise ValueError() #TODO: SMELL - Lazy Error Writing
        source = move.source
        destination = move.destination
        clone = self.clone()
        clone.board.setPiece(destination, self.board.pieceAt(source))
        clone.board.setPiece(source, "-")
        clone.isWhiteToMove = not self.isWhiteToMove
        if destination.y is None or source.y is None: raise ValueError #TODO: SMELL - Lazy Error Writing
        clone.enPassantPawn = destination if move.pieceType == "P" and abs(destination.y - source.y) == 2 else None
        clone.halfClock = (self.halfClock + 1) if not move.isCapture else 0
        clone.fullClock = self.fullClock + (0 if self.isWhiteToMove else 1)
        return clone


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