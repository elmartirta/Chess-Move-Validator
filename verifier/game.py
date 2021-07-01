from dataclasses import dataclass, field
from typing import List, Union
from verifier.castling_move import CastlingMove, UnfinishedCastlingMove
from .move import Move, UnfinishedMove
from .position import Position
from .notation_parser import NotationParser


@dataclass
class Game():
    startingPos: Position = NotationParser.fromStartingPosition()
    moves: List[Move] = field(default_factory=list)


@dataclass
class UnfinishedGame():
    startingPos: Position = NotationParser.fromStartingPosition()
    moves: List[UnfinishedMove] = field(default_factory=list)

    def append(self, move: UnfinishedMove):
        self.moves.append(move) 