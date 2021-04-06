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
        destination = Vector.fromAN(move.destination)
        for i in range(0,8):
            for line in ["vertical", "horizontal"]:
                if line == "vertical":
                    candidateVector = Vector(destination.x, i)
                elif line == "horizontal":
                    candidateVector = Vector(i, destination.y)
                else:
                    continue
                if candidateVector == destination: continue
                if position.pieceAt(candidateVector).upper() == move.pieceType:
                    moveList.append(move.clone().setSource(candidateVector))
    def addBishopCandidates(moveList, position, move):
        destination = Vector.fromAN(move.destination)
        for i in range(1,10):
            for diagonal in ["++", "+-", "-+", "--"]:
                if   diagonal == "++": candidateX, candidateY = destination.x+i, destination.y+i
                elif diagonal == "+-": candidateX, candidateY = destination.x+i, destination.y-i
                elif diagonal == "-+": candidateX, candidateY = destination.x-i, destination.y+i
                elif diagonal == "--": candidateX, candidateY = destination.x-i, destination.y-i
                else: 
                    continue
                if (candidateX >= 8 or candidateX <= 0 or candidateY >= 8 or candidateY <= 0):
                    continue
                candidateVector = Vector(candidateX, candidateY)
                if position.pieceAt(candidateVector).upper() == move.pieceType:
                    moveList.append(move.clone().setSource(candidateVector))
    def addKnightCandidates(moveList, position, move):
        destination = Vector.fromAN(move.destination)
        for m in [{"x": 1, "y": 2}, {"x": 2, "y": 1}]:
            for diagonal in ["++", "+-", "-+", "--"]:
                if   diagonal == "++": candidateX, candidateY = destination.x+m["x"], destination.y+m["y"]
                elif diagonal == "+-": candidateX, candidateY = destination.x+m["x"], destination.y-m["y"]
                elif diagonal == "-+": candidateX, candidateY = destination.x-m["x"], destination.y+m["y"]
                elif diagonal == "--": candidateX, candidateY = destination.x-m["x"], destination.y-m["y"]
                else:
                    continue
                if (candidateX >= 8 or candidateX <= 0 or candidateY >= 8 or candidateY <= 0):
                    continue
                candidateVector = Vector(candidateX, candidateY)
                if position.pieceAt(candidateVector).upper() == move.pieceType:
                    moveList.append(move.clone().setSource(candidateVector))
    def addKingCandidates(moveList, position, move):
        destination = Vector.fromAN(move.destination)
        for mx in [1,0,-1]:
            for my in [1,0,-1]:
                if mx != 0 or my != 0:
                    candidateX, candidateY = destination.x+mx, destination.y+my
                else:
                    continue
                if (candidateX >= 8 or candidateX <= 0 or candidateY >= 8 or candidateY <= 0):
                    continue
                candidateVector = Vector(candidateX, candidateY)
                if position.pieceAt(candidateVector).upper() == move.pieceType:
                    moveList.append(move.clone().setSource(candidateVector))
    def addQueenCandidates(moveList, position, move):
        MoveGenerator.addBishopCandidates(moveList, position, move)
        MoveGenerator.addRookCandidates(moveList, position, move)
    def addPawnCandidates(moveList, position, move):
        destination = Vector.fromAN(move.destination)
      
        candidates = []
        deduceCandidate = lambda movementVector: candidates.append(destination.plus(movementVector))
        if position.gameStatus == GameStatus.WHITE_TO_MOVE:
            if move.isCapture:
                deduceCandidate(Vector(-1,-1))
                deduceCandidate(Vector( 1,-1))
            else:
                if destination.y == 3:
                    deduceCandidate(Vector(0,-2))
                deduceCandidate(Vector(0,-1))
        elif position.gameStatus == GameStatus.BLACK_TO_MOVE:
            if move.isCapture:
                deduceCandidate(Vector(-1,1))
                deduceCandidate(Vector( 1,1))
            else:
                if destination.y == 4:
                    deduceCandidate(Vector(0,2))
                deduceCandidate(Vector(0,1))

        for candidate in candidates:
            candidateX = candidate.x
            candidateY = candidate.y
            if (candidateX > 7 or candidateX < 0 or candidateY > 7 or candidateY < 0):
                continue
            if (position.pieceAt(candidate).upper() == move.pieceType):
                moveList.append(move.clone().setSource(Vector(candidateX, candidateY)))

class MoveGenerationError(ValueError):
    def __init__(self, positionFEN, moveAN, errorMessage):
        super().__init__("Error trying to parse position \"%s\" and move %s. %s" % (positionFEN, moveAN, errorMessage))
