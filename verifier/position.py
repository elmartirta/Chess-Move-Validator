from __future__ import annotations
from typing import Optional
from verifier.castling_rights import CastlingRights
from .vector import Vector
from .board import Board
from .move import Move
from .castling_move import CastlingMove
from dataclasses import dataclass, replace


@dataclass
class Position():
    board: Board = Board()
    isWhiteToMove: bool = True
    castlingRights: CastlingRights = CastlingRights()
    enPassantPawn: Optional[Vector] = None
    halfClock: int = 0
    fullClock: int = 1
    
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
        clone = self.clone()
        clone.board.setPiece(move.midStep(), self.board.pieceAt(move.source))
        clone.board.setPiece(move.source, "-")
        return clone
    
    def finishCastle(self, move: CastlingMove) -> Position:
        clone = self.clone()
        clone.board.setPiece(move.destination, self.board.pieceAt(move.midStep()))
        clone.board.setPiece(move.midStep(), self.board.pieceAt(move.rookLocation))
        clone.board.setPiece(move.rookLocation, "-")
        clone.isWhiteToMove = not self.isWhiteToMove
        clone.enPassantPawn = None
        clone.halfClock = self.halfClock + 1 
        clone.fullClock = self.fullClock + (0 if self.isWhiteToMove else 1)
        return clone
    
    def next(self, move: Move) -> Position:
        source = move.source
        destination = move.destination
        clone = self.clone()
        clone.board.setPiece(destination, self.board.pieceAt(source))
        clone.board.setPiece(source, "-")
        clone.isWhiteToMove = not self.isWhiteToMove
        clone.enPassantPawn = destination if move.pieceType == "P" and abs(destination.y - source.y) == 2 else None
        clone.halfClock = (self.halfClock + 1) if not move.isCapture else 0
        clone.fullClock = self.fullClock + (0 if self.isWhiteToMove else 1)
        return clone