from move import Move
from position import *
from vector import Vector 
from castling_move import CastlingMove


class MoveFilter():
    def getPreMoveFilters():
        return [
            MoveFilter.checkSourcePiece,
            MoveFilter.checkIfMoveWithinLegalBounds,
            MoveFilter.checkIfDestinationIsOccupied,
            MoveFilter.checkIfPathIsOccupied,
            MoveFilter.checkIfCurrentKingInCheck
        ]

    def getMidCastleFilters():
        return [MoveFilter.checkIfCurrentKingInCheck]

    def getPostMoveFilters():
        return [MoveFilter.checkIfOppositeKingInCheck]

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

    def checkIfMoveWithinLegalBounds(position, move):
        if not move.destination.isInsideChessboard():
            return FilterResult.fail(
                    """Out of Bounds: The move's destination is not 
                    within the legal bounds of an 8x8 chessboard""",
                move)
        else:
            return FilterResult.accept(move)
 
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

    def checkIfCurrentKingInCheck(position, move):
        color = "WHITE" if position.isWhiteToMove else "BLACK"
        return MoveFilter.checkIfKingInCheck(position, move, color)

    def checkIfOppositeKingInCheck(position, move):
        color = "BLACK" if position.isWhiteToMove else "WHITE"
        return MoveFilter.checkIfKingInCheck(position, move, color)
        
    def checkIfKingInCheck(position, move, kingColor):
        kingSymbol = "K" if kingColor == "WHITE" else "k"
        if not any(kingSymbol in row for row in position.squares):
            raise FilterResult.fail(
                    """There is no king of the right color on the board""",
                move)
        kingLocations = position.findAll(kingSymbol)

        #TODO: SMELL - Repeated Code
        #The following for loop contains nested for loops that repeat code
        # (for rook ..., for bishop ..., for queen ...)
        for king in kingLocations:
            isEnemy = lambda enemy, enemyType: \
                position.pieceTypeIs(enemy, enemyType) \
                and position.pieceIsWhite(enemy) != position.pieceIsWhite(king) \
                and all(position.isEmptyAt(tile) for tile in king.between(enemy)) 
            xLine = [Vector(king.x, y) for y in range(0,8)]
            yLine = [Vector(x, king.y) for x in range(0,8)]
            orthogonals = xLine + yLine
            for rook in orthogonals:
                if rook != king and isEnemy(rook, "R"): 
                    return FilterResult.fail(
                            "The king on %s is being checked by the rook on %s"
                            % (king, rook),
                        move) 
            posPos = [king.plus( i, i) for i in range(1,8) if (king.plus( i, i)).isInsideChessboard()]
            posNeg = [king.plus(-i, i) for i in range(1,8) if (king.plus(-i, i)).isInsideChessboard()]
            NegPos = [king.plus( i,-i) for i in range(1,8) if (king.plus( i,-i)).isInsideChessboard()]
            NegNeg = [king.plus(-i,-i) for i in range(1,8) if (king.plus(-i,-i)).isInsideChessboard()]
            diagonals = posPos + posNeg + NegPos + NegNeg
            for bishop in diagonals:
                if bishop != king and isEnemy(bishop, "B"): 
                    return FilterResult.fail(
                            "The king on %s is being checked by the bishop on %s"
                            % (king, bishop),
                        move)
            for queen in orthogonals + diagonals:
                if queen != king and isEnemy(queen, "Q"): 
                    return FilterResult.fail(
                            "The king on %s is being checked by the queen on %s"
                            % (king, queen),
                        move)
            knightSquares = [king + deltaN for deltaN in [
                    Vector( 1 , 2),
                    Vector(-1 , 2),
                    Vector( 1 ,-2),
                    Vector(-1 ,-2),
                    Vector( 2 , 1),
                    Vector(-2 , 1),
                    Vector( 2 ,-1),
                    Vector(-2 ,-1)
                ] if (king + deltaN).isInsideChessboard()]
            for knight in knightSquares:
                if isEnemy(knight, "n"):
                    return FilterResult.fail(
                            "The king on %s is being checked by the knight on %s"
                            % (king, knight),
                        move)
            blackPawns = [king + delta for delta in [Vector(1, 1), Vector(-1, 1)] if (king + delta).isInsideChessboard()]
            whitePawns = [king + delta for delta in [Vector(1,-1), Vector(-1,-1)] if (king + delta).isInsideChessboard()]
            pawns = blackPawns if kingColor == "WHITE" else whitePawns
            for pawn in pawns:
                if isEnemy(pawn, "p"):
                    return FilterResult.fail(
                            "The king on %s is being checked by the pawn on %s"
                            % (king, pawn),
                        move)
            return FilterResult.accept(move)  


class FilterResult():
    def __init__(self, reason, move, isLegal=True):
        self.reason = reason
        self.move = move
        self.isLegal = isLegal

    def accept(move):
        return FilterResult("", move, True)

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
