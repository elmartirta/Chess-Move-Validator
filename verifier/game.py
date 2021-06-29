from dataclasses import dataclass, field
from typing import List
from .move import Move
from .position import Position
from .notation_parser import NotationParser
@dataclass
class Game():
    moves: List[Move] = field(default_factory=list)
    startingPos: Position = NotationParser.fromStartingPosition()