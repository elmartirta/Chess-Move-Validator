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

        def checkFor(attackerType, kingLocation, candidates):
            for candidate in candidates:
                if candidate != kingLocation \
                        and board.pieceTypeIs(candidate, attackerType) \
                        and board.pieceIsWhite(candidate) != kingIsWhite \
                        and (
                            attackerType not in "RBQ" \
                            or board.pieceCanSee(candidate, king)):
                    return FilterResult.fail(
                            "The king on %s is being checked by the %s on %s"
                            % (king.toAN(), attackerType, candidate.toAN()),
                        move)

        error = None
        for king in kingLocations:
            error = error or checkFor("R", king, board.getOrthogonalsTargeting(king))
            error = error or checkFor("B", king, board.getDiagonalsTargeting(king))
            error = error or checkFor("Q", king, board.getOrthogonalsTargeting(king) + board.getDiagonalsTargeting(king))
            error = error or checkFor("N", king, board.getKnightSquaresTargeting(king))

            pawns = board.getBlackPawnsTargeting(king) if kingIsWhite else board.getWhitePawnsTargeting(king)
            error = error or  checkFor("P", king, pawns)
            
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
                "The move %s fails the filtration process because: %s"
                % (move, reason),
            move, False)


class FilterError(ValueError):
    def __init__(self, reason: str, move: Move):
        super().__init__(
            "The move %s is unable to be properly filtered, because: %s" \
            % (move, reason))