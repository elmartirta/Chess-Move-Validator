from move import Move
from enum import Enum

class CastlingMove(Move):
    def __init__(self, pieceType, source, destination, isCapture, isCheck, isCheckmate, promotionPiece, castlingDirection, rookLocation):
        super().__init__(pieceType, source, destination, isCapture, isCheck, isCheckmate, promotionPiece)
        self.castlingDirection = castlingDirection
        self.rookLocation = rookLocation

class CastlingDirection(Enum):
    KINGSIDE = 1
    QUEENSIDE = 2
