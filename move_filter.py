from move import Move
from position import *
from vector2D import Vector2D as Vector

class MoveFilter():
    def getPreMoveFilters():
        return [
            MoveFilter.checkSourcePiece,
            MoveFilter.checkIfMoveWithinLegalBounds,
            MoveFilter.checkIfDestinationIsOccupied,
            MoveFilter.checkIfPathIsOccupied
        ]
    def getPostMoveFilters():
        return []
    def checkSourcePiece(position, move):
        if move.sourceRank == None:
            raise FilterError(move, "Which Piece? The Source Rank is not instantiated, leading to ambiguity.")
        elif move.sourceFile == None:
            raise FilterError(move, "Which Piece? The Source file is not instantiated, leading to ambiguity.")
        elif position.pieceIsWhite(move.source()) != position.isWhiteToMove():
            return FilterResult.fail(move, "Not your turn: The color of the move's source piece is not valid in the turn order.")
        elif position.pieceTypeOf(move.source()) != move.pieceType:
            raise FilterError( \
                move, "Hustler's Piece: Type of source Piece (%s) does not match type of move piece (%s)." \
                % (position.pieceTypeOf(move.source()), move.pieceType)
            )
        else:
            return FilterResult.accept(move)

    def checkIfMoveWithinLegalBounds(position, move):
        if not move.destination.isInsideChessboard():
            return FilterResult.fail(move, "Out of Bounds: The move's destination is not within the legal bounds of an 8x8 chessboard")
        else:
            return FilterResult.accept(move)
 
    def checkIfDestinationIsOccupied(position, move):
        if move.isCapture and (position.pieceIsWhite(move.destination) == positon.isWhiteToMove()):
            return FilterResult.fail(move, "Friendly Fire: The move involves a piece trying to capture a target of the same color.")
        elif move.isCapture and position.pieceAt(move.destination) == "-":
            return FilterResult.fail(move, "Starved Attacker: Move is a capture, but there is no piece to capture on the destination square")
        elif not move.isCapture and not position.pieceAt(move.destination) == "-":
            return FilterResult.fail(move, "Cramped Quarters: The Move is not a capture, and the destination is not empty")
        else:
            return FilterResult.accept(move)
    
    def checkIfPathIsOccupied(position, move):
        if move.pieceType in "N":
            return FilterResult.accept(move)
        
        path = move.destination - move.source()
        for delta in path.walk():
            candidate = move.source() + delta
            if position.pieceAt(candidate) != "-":
                return FilterResult.fail(move, \
                    "Obstructed: The piece %s at %s in the way of the move." \
                    % (position.pieceAt(candidate), candidate.toAN()))
        return FilterResult.accept(move)


class FilterResult():
    def __init__(self, move, isLegal=True, reason=""):
        self.move = move
        self.isLegal = isLegal
        self.reason = reason
    def accept(move):
        return FilterResult(move, True, "")
    def fail(move, reason):
        return FilterResult(move, False,
            "The move %s fails the filtration process because: %s" % (move, reason)
        )


class FilterError(ValueError):
    def __init__(self, move, reason):
        super().__init__("The move %s is unable to be properly filtered, because: %s" % (move, reason))
