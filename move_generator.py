from position import Position
from position import GameStatus
from move import Move
from vector2D import Vector2D as Vector
class MoveGenerator():
    def generateMoveListFromFEN(positionFEN, moveAN):
        position = Position.fromFEN(positionFEN)
        move = Move.fromAN(moveAN)

        moveList = []
        if move.pieceType == None: 
            raise MoveGenerationError(positionFEN, moveAN, "PieceType is None")
        if   (move.pieceType in "rR"): MoveGenerator.addRookCandidates(moveList, position, move)
        elif (move.pieceType in "bB"): MoveGenerator.addBishopCandidates(moveList, position, move)
        elif (move.pieceType in "qQ"): MoveGenerator.addQueenCandidates(moveList, position, move)
        elif (move.pieceType in "nN"): MoveGenerator.addKnightCandidates(moveList, position, move)
        elif (move.pieceType in "kK"): MoveGenerator.addKingCandidates(moveList, position, move)
        elif (move.pieceType in "pP"): MoveGenerator.addPawnCandidates(moveList, position, move)
        else:
            raise MoveGenerationError(positionFEN, moveAN, "Unsupported Piece type: " + move.pieceType)
        return moveList
    
    def addRookCandidates(moveList, position, move):
        for i in range(0,8):
            for candidate in [
                    Vector(move.destination.x, i), 
                    Vector(i, move.destination.y)]:
                if candidate == move.destination: 
                    continue
                if position.pieceAt(candidate).upper() == move.pieceType:
                    moveList.append(move.clone().setSource(candidate))
    def addBishopCandidates(moveList, position, move):
        for i in range(1,10):
            for delta in [
                    Vector( i, i),
                    Vector(-i, i),
                    Vector( i,-i),
                    Vector(-i,-i)]:
                candidate = move.destination + delta
                if candidate.isInsideChessboard() and position.pieceAt(candidate).upper() == move.pieceType:
                    moveList.append(move.clone().setSource(candidate))
    def addKnightCandidates(moveList, position, move):
        for n in [Vector(1,2), Vector(2,1)]:
            for delta in [
                    Vector( n.x, n.y),
                    Vector(-n.x, n.y),
                    Vector( n.x,-n.y),
                    Vector(-n.x,-n.y)]:
                candidate = move.destination + delta
                if candidate.isInsideChessboard() and position.pieceAt(candidate).upper() == move.pieceType:
                    moveList.append(move.clone().setSource(candidate))
    def addKingCandidates(moveList, position, move):
        for dx in [1,0,-1]:
            for dy in [1,0,-1]:
                if dx == 0 and dy == 0: continue
                delta = Vector(dx, dy)
                candidate = move.destination + delta
                if candidate.isInsideChessboard() and position.pieceAt(candidate).upper() == move.pieceType:
                    moveList.append(move.clone().setSource(candidate))
    def addQueenCandidates(moveList, position, move):
        MoveGenerator.addBishopCandidates(moveList, position, move)
        MoveGenerator.addRookCandidates(moveList, position, move)
    def addPawnCandidates(moveList, position, move):
        destination = move.destination
      
        deltas = []
        dy = -1 if position.gameStatus == GameStatus.WHITE_TO_MOVE else 1
        if move.isCapture:
            deltas.append(Vector(-1,dy))
            deltas.append(Vector( 1,dy))
        else:
            deltas.append(Vector(0,dy))
            if (destination.y == 3 and position.gameStatus == GameStatus.WHITE_TO_MOVE) or \
                    (destination.y == 4 and position.gameStatus == GameStatus.BLACK_TO_MOVE):
                deltas.append(Vector(0,2*dy))

        for delta in deltas:
            candidate = move.destination + delta
            if candidate.isInsideChessboard() and position.pieceAt(candidate).upper() == move.pieceType:
                moveList.append(move.clone().setSource(candidate))

class MoveGenerationError(ValueError):
    def __init__(self, positionFEN, moveAN, errorMessage):
        super().__init__("Error trying to parse position \"%s\" and move %s. %s" % (positionFEN, moveAN, errorMessage))
