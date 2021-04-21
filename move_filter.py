from move import Move
from position import *
from vector import Vector 
from castling_move import CastlingMove, CastlingDirection

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
        return [
            MoveFilter.checkIfCurrentKingInCheck
        ]
    def getPostMoveFilters():
        return [
            MoveFilter.checkIfOppositeKingInCheck
        ]
    def checkSourcePiece(position, move):
        #TODO: SMELL - Line Length
        if move.source.x == None or move.source.y == None:
            raise FilterError(move, "Which Piece? The Source file is not instantiated, leading to ambiguity.")
        elif position.pieceIsWhite(move.source) != position.isWhiteToMove():
            return FilterResult.fail(move, "Not your turn: The color of the move's source piece is not valid in the turn order.")
        elif position.pieceTypeOf(move.source) != move.pieceType:
            raise FilterError( \
                move, "Hustler's Piece: Type of source Piece (%s) does not match type of move piece (%s)." \
                % (position.pieceTypeOf(move.source), move.pieceType)
            )
        else:
            return FilterResult.accept(move)

    def checkIfMoveWithinLegalBounds(position, move):
        #TODO: SMELL - Line Length
        if not move.destination.isInsideChessboard():
            return FilterResult.fail(move, "Out of Bounds: The move's destination is not within the legal bounds of an 8x8 chessboard")
        else:
            return FilterResult.accept(move)
 
    def checkIfDestinationIsOccupied(position, move):
        #TODO: SMELL - Line Length
        if move.isCapture and (position.pieceIsWhite(move.destination) == position.isWhiteToMove()):
            return FilterResult.fail(move, "Friendly Fire: The move involves a piece trying to capture a target of the same color.")
        elif move.isCapture and position.pieceAt(move.destination) == "-":
            return FilterResult.fail(move, "Starved Attacker: Move is a capture, but there is no piece to capture on the destination square")
        elif not move.isCapture and not position.pieceAt(move.destination) == "-":
            return FilterResult.fail(move, "Cramped Quarters: The Move is not a capture, and the destination is not empty")
        elif isinstance(move, CastlingMove):
            midStep = move.source + (Vector(1,0) if move.castlingDirection == CastlingDirection.KINGSIDE else Vector(-1,0))
            if not position.pieceAt(midStep) == "-":
                return FilterResult.fail(move, "Castling Blocked: There is a piece between the king's source and destination squares.")
        
        return FilterResult.accept(move)
    
    def checkIfPathIsOccupied(position, move):
        if move.pieceType in "N":
            return FilterResult.accept(move)

        for candidate in move.source.between(move.destination):
            if position.pieceAt(candidate) != "-":
                return FilterResult.fail(move, \
                    "Obstructed: The piece %s at %s in the way of the move." \
                    % (position.pieceAt(candidate), candidate.toAN()))
        return FilterResult.accept(move)

    def checkIfCurrentKingInCheck(position, move):
        color = "WHITE" if position.gameStatus == GameStatus.WHITE_TO_MOVE else "BLACK"
        return MoveFilter.checkIfKingInCheck(position, move, color)

    def checkIfOppositeKingInCheck(position, move):
        color = "BLACK" if position.gameStatus == GameStatus.WHITE_TO_MOVE else "WHITE"
        return MoveFilter.checkIfKingInCheck(position, move, color)
        
    def checkIfKingInCheck(position, move, kingColor):
        #TODO: SMELL - Line Length
        if not any(("K" if kingColor == "WHITE" else "k") in row for row in position.boardState.squares):
            raise FilterError(move, "There is no king of the right color on the board")
        kingLocations = position.findAll("K" if kingColor == "WHITE" else "k")

        for king in kingLocations:
            isEnemy = lambda enemy, enemyType: \
                position.pieceTypeIs(enemy, enemyType) \
                and position.pieceIsWhite(enemy) != position.pieceIsWhite(king) \
                and all(position.pieceAt(tile) == "-" for tile in king.between(enemy))

            xLine = [Vector(king.x, y) for y in range(0,8)]
            yLine = [Vector(x, king.y) for x in range(0,8)]
            orthogonals = xLine + yLine

            for rook in orthogonals:
                if rook != king and isEnemy(rook, "R"): 
                    return FilterResult.fail(move, "The king on %s is being checked by the rook on %s" % (king, rook))
            #TODO: SMELL - Line Length
            posPos = [king + Vector( i, i) for i in range(1,8) if (king + Vector( i, i)).isInsideChessboard()]
            posNeg = [king + Vector(-i, i) for i in range(1,8) if (king + Vector(-i, i)).isInsideChessboard()]
            NegPos = [king + Vector( i,-i) for i in range(1,8) if (king + Vector( i,-i)).isInsideChessboard()]
            NegNeg = [king + Vector(-i,-i) for i in range(1,8) if (king + Vector(-i,-i)).isInsideChessboard()]
            diagonals = posPos + posNeg + NegPos + NegNeg

            for bishop in diagonals:
                if bishop != king and isEnemy(bishop, "B"): 
                    return FilterResult.fail(move, "The king on %s is being checked by the bishop on %s" % (king, bishop))
            
            for queen in orthogonals + diagonals:
                if queen != king and isEnemy(queen, "Q"): 
                    return FilterResult.fail(move, "The king on %s is being checked by the queen on %s" % (king, queen))

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
                    return FilterResult.fail(move, "The king on %s is being checked by the knight on %s" % (king, knight))
            #TODO: SMELL - Line Length
            blackPawns = [king + deltaP for deltaP in [Vector(1, 1), Vector(-1, 1)] if (king + deltaP).isInsideChessboard()]
            whitePawns = [king + deltaP for deltaP in [Vector(1,-1), Vector(-1,-1)] if (king + deltaP).isInsideChessboard()]
            pawns = blackPawns if kingColor == "WHITE" else whitePawns

            for pawn in pawns:
                if isEnemy(pawn, "p"):
                    return FilterResult.fail(move, "The king on %s is being checked by the pawn on %s" % (king, pawn))

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
        #TODO: SMELL - Line Length
        super().__init__("The move %s is unable to be properly filtered, because: %s \n %s" % (move, reason, position.boardState.toString()))
