from move import Move
from position import *
from vector import Vector 
from castling_move import CastlingMove
import pdb

class MoveFilter():
    @staticmethod
    def getPreMoveFilters():
        return [
            MoveFilter.checkSourcePiece,
            MoveFilter.checkIfMoveWithinLegalBounds,
            MoveFilter.checkIfDestinationIsOccupied,
            MoveFilter.checkIfPathIsOccupied,
            MoveFilter.checkIfCurrentKingInCheck
        ]

    @staticmethod
    def getMidCastleFilters():
        return [MoveFilter.checkIfCurrentKingInCheck]

    @staticmethod
    def getPostMoveFilters():
        return [MoveFilter.checkIfOppositeKingInCheck]

    @staticmethod
    def checkSourcePiece(position, move):
        if move.source.x == None or move.source.y == None:
            raise FilterError(
                    """Which Piece? The Source file is not instantiated, 
                    leading to ambiguity.""",
                move) 
        elif position.pieceTypeOf(move.source) != move.pieceType:
            raise FilterError(
                    """Hustler's Piece: Type of source Piece 
                    (%s) does not match type of move piece (%s)."""
                    % (position.pieceTypeOf(move.source), move.pieceType),
                move)
        elif position.pieceIsWhite(move.source) != position.isWhiteToMove:
            return FilterResult.fail(
                    """Wrong Color: The color of the move's 
                    source piece does not match the color that
                    is moving right now.""",
                move) 
        else:
            return FilterResult.accept(move)

    @staticmethod
    def checkIfMoveWithinLegalBounds(position, move):
        if not move.destination.isInsideChessboard():
            return FilterResult.fail(
                    """Out of Bounds: The move's destination is not 
                    within the legal bounds of an 8x8 chessboard""",
                move)
        else:
            return FilterResult.accept(move)
 
    @staticmethod
    def checkIfDestinationIsOccupied(position, move):
        if move.isCapture and (position.pieceIsWhite(move.destination) == position.isWhiteToMove):
            return FilterResult.fail(
                    """Friendly Fire: The move involves a piece trying to 
                    capture a target of the same color.""",
                move)
        elif move.isCapture and position.isEmptyAt(move.destination):
            return FilterResult.fail(
                    """Starved Attacker: Move is a capture, but there is no 
                    piece to capture on the destination square""",
                move)
        elif not move.isCapture and not position.isEmptyAt(move.destination):
            return FilterResult.fail(
                    """Cramped Quarters: The Move is not a capture,
                    and the destination is not empty""",
                move)
        elif isinstance(move, CastlingMove):
            if not position.isEmptyAt(move.midStep()):
                return FilterResult.fail(
                        """Castling Blocked: There is a piece between the 
                        king's source and destination squares.""",
                    move) 
        return FilterResult.accept(move)
    
    @staticmethod
    def checkIfPathIsOccupied(position, move):
        if move.pieceType in "N":
            return FilterResult.accept(move)
        for candidate in move.source.between(move.destination):
            if not position.isEmptyAt(candidate):
                return FilterResult.fail(
                        """Obstructed: The piece %s at %s in the way of the move."""
                        % (position.pieceAt(candidate), candidate.toAN()),
                    move)
        return FilterResult.accept(move)

    @staticmethod
    def checkIfCurrentKingInCheck(position, move):
        return MoveFilter._checkIfKingInCheck(position, move, position.isWhiteToMove)

    @staticmethod
    def checkIfOppositeKingInCheck(position, move):
        return MoveFilter._checkIfKingInCheck(position, move, not position.isWhiteToMove)
        
    @staticmethod
    def _checkIfKingInCheck(position, move, kingIsWhite):
        kingSymbol = "K" if kingIsWhite else "k"
        if not any(kingSymbol in row for row in position.squares):
            raise FilterResult.fail(
                    """There is no king of the right color on the board""",
                move)
        kingLocations = position.findAll(kingSymbol)

        def checkFor(attackerType, kingLocation, candidates):
            for candidate in candidates:
                if candidate != kingLocation \
                        and position.pieceTypeIs(candidate, attackerType) \
                        and position.pieceIsWhite(candidate) != kingIsWhite \
                        and (
                            attackerType not in "RBQ" \
                            or all(position.isEmptyAt(tile) for tile in king.between(candidate))):
                    return FilterResult.fail(
                            "The king on %s is being checked by the %s on %s"
                            % (king.toAN(), attackerType, candidate.toAN()),
                        move)

        for king in kingLocations:
            error = None
            error = error or checkFor("R", king, position.getOrthogonalsTargeting(king))
            error = error or checkFor("B", king, position.getDiagonalsTargeting(king))
            error = error or checkFor("Q", king, position.getOrthogonalsTargeting(king) + position.getDiagonalsTargeting(king))
            error = error or checkFor("N", king, position.getKnightSquaresTargeting(king))

            pawns = position.getBlackPawnsTargeting(king) if kingIsWhite else position.getWhitePawnsTargeting(king)
            error = error or  checkFor("P", king, pawns)
            
            if error: 
                return error
            else:
                return FilterResult.accept(move)  


class FilterResult():
    def __init__(self, reason, move, isLegal=True):
        self.reason = reason
        self.move = move
        self.isLegal = isLegal

    @staticmethod
    def accept(move):
        return FilterResult("", move, True)

    @staticmethod
    def fail(reason, move):
        assert(isinstance(reason, str))
        return FilterResult(
                "The move %s fails the filtration process because: %s"
                % (move, reason),
            move, False)


class FilterError(ValueError):
    def __init__(self, reason, move):
        super().__init__(
            "The move %s is unable to be properly filtered, because: %s" \
            % (move, reason))
