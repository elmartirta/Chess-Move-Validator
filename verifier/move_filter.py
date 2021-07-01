from __future__ import annotations
from typing import Callable, List
from .position import *
from .castling_move import CastlingMove

class MoveFilter():
    @staticmethod
    def getPreMoveFilters() -> List[Callable[[Position, Move], FilterResult]]:
        return [
            MoveFilter.checkSourcePiece,
            MoveFilter.checkIfMoveWithinLegalBounds,
            MoveFilter.checkIfDestinationIsOccupied,
            MoveFilter.checkIfPathIsOccupied,
            MoveFilter.checkIfCurrentKingInCheck
        ]

    @staticmethod
    def getMidCastleFilters() -> List[Callable[[Position, Move], FilterResult]]:
        return [MoveFilter.checkIfCurrentKingInCheck]

    @staticmethod
    def getPostMoveFilters() -> List[Callable[[Position, Move], FilterResult]]:
        return [MoveFilter.checkIfOppositeKingInCheck]

    @staticmethod
    def checkSourcePiece(position: Position, move: Move) -> FilterResult:
        if isinstance(move.source, UnfinishedVector):
            raise FilterError(
                    """Which Piece? The Source file is not instantiated, 
                    leading to ambiguity.""",
                move) 
        elif position.board.pieceTypeOf(move.source) != move.pieceType:
            raise FilterError(
                    """Hustler's Piece: Type of source Piece 
                    (%s) does not match type of move piece (%s)."""
                    % (position.board.pieceTypeOf(move.source), move.pieceType),
                move)
        elif position.board.pieceIsWhite(move.source) != position.isWhiteToMove:
            return FilterResult.fail(
                    """Wrong Color: The color of the move's 
                    source piece does not match the color that
                    is moving right now.""",
                move) 
        else:
            return FilterResult.accept(move)

    @staticmethod
    def checkIfMoveWithinLegalBounds(position: Position, move: Move) -> FilterResult:
        if not move.destination.isInsideChessboard():
            return FilterResult.fail(
                    """Out of Bounds: The move's destination is not 
                    within the legal bounds of an 8x8 chessboard""",
                move)
        else:
            return FilterResult.accept(move)
 
    @staticmethod
    def checkIfDestinationIsOccupied(position: Position, move: Move) -> FilterResult:
        if move.isCapture and (position.board.pieceIsWhite(move.destination) == position.isWhiteToMove):
            return FilterResult.fail(
                    """Friendly Fire: The move involves a piece trying to 
                    capture a target of the same color.""",
                move)
        elif move.isCapture and position.board.isEmptyAt(move.destination):
            return FilterResult.fail(
                    """Starved Attacker: Move is a capture, but there is no 
                    piece to capture on the destination square""",
                move)
        elif not move.isCapture and not position.board.isEmptyAt(move.destination):
            return FilterResult.fail(
                    """Cramped Quarters: The Move is not a capture,
                    and the destination is not empty""",
                move)
        elif isinstance(move, CastlingMove):
            if not position.board.isEmptyAt(move.midStep()):
                return FilterResult.fail(
                        """Castling Blocked: There is a piece between the 
                        king's source and destination squares.""",
                    move) 
        return FilterResult.accept(move)
    
    @staticmethod
    def checkIfPathIsOccupied(position: Position, move: Move) -> FilterResult:
        if move.pieceType in "N":
            return FilterResult.accept(move)
        if not position.board.pieceCanSee(move.source, move.destination):
            return FilterResult.fail(
                    """Obstructed: A piece is in the way of the move.""",
                move)
        return FilterResult.accept(move)

    @staticmethod
    def checkIfCurrentKingInCheck(position: Position, move: Move) -> FilterResult:
        return MoveFilter._checkIfKingInCheck(position.board, move, position.isWhiteToMove)

    @staticmethod
    def checkIfOppositeKingInCheck(position: Position, move: Move) -> FilterResult:
        return MoveFilter._checkIfKingInCheck(position.board, move, not position.isWhiteToMove)
        
    @staticmethod
    def _checkIfKingInCheck(board: Board, move: Move, kingIsWhite: bool) -> FilterResult:
        kingSymbol = "K" if kingIsWhite else "k"
        if len(board.findAll(kingSymbol)) == 0:
            return FilterResult.fail(
                    """There is no king of the right color on the board""",
                move)
        kingLocations = board.findAll(kingSymbol)

        def checkFor(kingLocation, candidates):
            for candidate in candidates:
                if candidate != kingLocation \
                        and board.pieceIsWhite(candidate) != kingIsWhite \
                        and (
                            board.pieceTypeOf(candidate) not in "RBQ" \
                            or board.pieceCanSee(candidate, king)):
                    return FilterResult.fail(
                            "The king on %s is being checked by the piece on %s"
                            % (king.toAN(), candidate.toAN()),
                        move)

        error = None
        for king in kingLocations:
            error = error or checkFor(king, board.getRooksAttacking(king))
            error = error or checkFor(king, board.getBishopsAttacking(king))
            error = error or checkFor(king, board.getQueensAttacking(king))
            error = error or checkFor(king, board.getKnightsAttacking(king))
            error = error or checkFor(king, board.getPawnsAttacking(king))
            
        if error: 
            return error
        else:
            return FilterResult.accept(move)  

@dataclass
class FilterResult():
    reason: str
    move: Move
    isLegal: bool = True

    @staticmethod
    def accept(move: Move) -> FilterResult:
        return FilterResult("", move, True)

    @staticmethod
    def fail(reason: str, move: Move) -> FilterResult:
        assert(isinstance(reason, str))
        return FilterResult(
                f"The move {move} fails the filtration process because: {reason}",
            move, False)


class FilterError(ValueError):
    def __init__(self, reason: str, move: Move):
        super().__init__(
            f"The move {move} is unable to be properly filtered, because: {reason}")
