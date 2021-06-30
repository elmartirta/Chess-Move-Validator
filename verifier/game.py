from dataclasses import dataclass, field
from typing import List, Union
from verifier.castling_move import CastlingMove, UnfinishedCastlingMove
from .move import Move, UnfinishedMove
from .position import Position
from .notation_parser import NotationParser


@dataclass
class Game():
    startingPos: Position = NotationParser.fromStartingPosition()
    moves: List[Union[Move, CastlingMove]] = field(default_factory=list)


@dataclass
class UnfinishedGame():
    startingPos: Position = NotationParser.fromStartingPosition()
    moves: List[Union[Move, UnfinishedMove, CastlingMove, UnfinishedCastlingMove]] = field(default_factory=list)

    def append(self, move: Union[UnfinishedMove, UnfinishedCastlingMove]):
        self.moves.append(move) 