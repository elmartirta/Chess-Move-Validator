from __future__ import annotations
from typing import Callable, List
from .position import *
from .castling_move import CastlingMove

class Constraints():
    @staticmethod
    def getPreMoveConstraints() -> List[Callable[[Position, Move], ConstraintResult]]:
        return [
            Constraints.sourcePieceExists,
            Constraints.sourceTypeMatchesNotation,
            Constraints.moveWithinLegalBounds,
            Constraints.destinationUnoccupied,
            Constraints.pathUnoccupied,
            Constraints.currentKingNotInCheck
        ]

    @staticmethod
    def getMidCastleConstraints() -> List[Callable[[Position, Move], ConstraintResult]]:
        return [Constraints.currentKingNotInCheck]

    @staticmethod
    def getPostMoveConstraints() -> List[Callable[[Position, Move], ConstraintResult]]:
        return [Constraints.oppositeKingNotInCheck]

    @staticmethod
    def sourcePieceExists(_: Position, move: Move) -> ConstraintResult:
        if isinstance(move.source, UnfinishedVector):
            raise ConstraintError(
                    """Which Piece? The Source file is not instantiated, 
                    leading to ambiguity.""",
                move)
        return ConstraintResult.accept(move)
    
    @staticmethod
    def sourceTypeMatchesNotation(position: Position, move: Move) -> ConstraintResult:
        if position.board.pieceTypeOf(move.source) != move.pieceType:
            raise ConstraintError(
                    """Hustler's Piece: Type of source Piece 
                    (%s) does not match type of move piece (%s)."""
                    % (position.board.pieceTypeOf(move.source), move.pieceType),
                move)
        elif position.board.pieceIsWhite(move.source) != position.isWhiteToMove:
            return ConstraintResult.fail(
                    """Wrong Color: The color of the move's 
                    source piece does not match the color that
                    is moving right now.""",
                move) 
        else:
            return ConstraintResult.accept(move)

    @staticmethod
    def moveWithinLegalBounds(position: Position, move: Move) -> ConstraintResult:
        if not move.destination.isInsideChessboard():
            return ConstraintResult.fail(
                    """Out of Bounds: The move's destination is not 
                    within the legal bounds of an 8x8 chessboard""",
                move)
        else:
            return ConstraintResult.accept(move)
 
    @staticmethod
    def destinationUnoccupied(position: Position, move: Move) -> ConstraintResult:
        if move.isCapture and (position.board.pieceIsWhite(move.destination) == position.isWhiteToMove):
            return ConstraintResult.fail(
                    """Friendly Fire: The move involves a piece trying to 
                    capture a target of the same color.""",
                move)
        elif move.isCapture and position.board.isEmptyAt(move.destination):
            return ConstraintResult.fail(
                    """Starved Attacker: Move is a capture, but there is no 
                    piece to capture on the destination square""",
                move)
        elif not move.isCapture and not position.board.isEmptyAt(move.destination):
            return ConstraintResult.fail(
                    """Cramped Quarters: The Move is not a capture,
                    and the destination is not empty""",
                move)
        elif isinstance(move, CastlingMove):
            if not position.board.isEmptyAt(move.midStep()):
                return ConstraintResult.fail(
                        """Castling Blocked: There is a piece between the 
                        king's source and destination squares.""",
                    move) 
        return ConstraintResult.accept(move)
    
    @staticmethod
    def pathUnoccupied(position: Position, move: Move) -> ConstraintResult:
        if move.pieceType in "N":
            return ConstraintResult.accept(move)
        if not position.board.pieceCanSee(move.source, move.destination):
            return ConstraintResult.fail(
                    """Obstructed: A piece is in the way of the move.""",
                move)
        return ConstraintResult.accept(move)

    @staticmethod
    def currentKingNotInCheck(position: Position, move: Move) -> ConstraintResult:
        return Constraints._checkIfKingInCheck(position.board, move, position.isWhiteToMove)

    @staticmethod
    def oppositeKingNotInCheck(position: Position, move: Move) -> ConstraintResult:
        return Constraints._checkIfKingInCheck(position.board, move, not position.isWhiteToMove)
        
    @staticmethod
    def _checkIfKingInCheck(board: Board, move: Move, kingIsWhite: bool) -> ConstraintResult:
        kingSymbol = "K" if kingIsWhite else "k"
        if len(board.findAll(kingSymbol)) == 0:
            return ConstraintResult.fail(
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
                    return ConstraintResult.fail(
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
            return ConstraintResult.accept(move)  

@dataclass
class ConstraintResult():
    reason: str
    move: Move
    isLegal: bool = True

    @staticmethod
    def accept(move: Move) -> ConstraintResult:
        return ConstraintResult("", move, True)

    @staticmethod
    def fail(reason: str, move: Move) -> ConstraintResult:
        assert(isinstance(reason, str))
        return ConstraintResult(
                f"The move {move} fails the filtration process because: {reason}",
            move, False)


class ConstraintError(ValueError):
    def __init__(self, reason: str, move: Move):
        super().__init__(
            f"The move {move} is unable to be properly filtered, because: {reason}")
