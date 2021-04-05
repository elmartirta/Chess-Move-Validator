from position import Position
from position import GameStatus
from move import Move
from cartesian_coordinate import CartesianCoordinate as Coordinate
class MoveVerifier():
    def generateMoveListFromFEN(positionFEN, moveAN):
        position = Position.fromFEN(positionFEN)
        move = Move.fromAN(moveAN)

        moveList = []
        if move.pieceType == None: 
            raise MoveGenerationError(positionFEN, moveAN, "PieceType is None")
        if   (move.pieceType in "rR"): MoveVerifier.addRookCandidates(moveList, position, move)
        elif (move.pieceType in "bB"): MoveVerifier.addBishopCandidates(moveList, position, move)
        elif (move.pieceType in "qQ"): MoveVerifier.addQueenCandidates(moveList, position, move)
        elif (move.pieceType in "nN"): MoveVerifier.addKnightCandidates(moveList, position, move)
        elif (move.pieceType in "kK"): MoveVerifier.addKingCandidates(moveList, position, move)
        elif (move.pieceType in "pP"): MoveVerifier.addPawnCandidates(moveList, position, move)
        else:
            raise MoveGenerationError(positionFEN, moveAN, "Unsupported Piece type: " + move.pieceType)
        return moveList
    
    def addRookCandidates(moveList, position, move):
        destination = Coordinate.fromAN(move.destination)
        for i in range(0,8):
            for line in ["vertical", "horizontal"]:
                if line == "vertical":
                    candidateCoordinate = Coordinate(destination.x, i)
                elif line == "horizontal":
                    candidateCoordinate = Coordinate(i, destination.y)
                else:
                    continue
                if position.pieceAt(candidateCoordinate).upper() == move.pieceType:
                    moveList.append(move.clone().setSource(candidateCoordinate))
    def addBishopCandidates(moveList, position, move):
        destination = Coordinate.fromAN(move.destination)
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
                candidateCoordinate = Coordinate(candidateX, candidateY)
                if position.pieceAt(candidateCoordinate).upper() == move.pieceType:
                    moveList.append(move.clone().setSource(candidateCoordinate))
    def addKnightCandidates(moveList, position, move):
        destination = Coordinate.fromAN(move.destination)
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
                candidateCoordinate = Coordinate(candidateX, candidateY)
                if position.pieceAt(candidateCoordinate).upper() == move.pieceType:
                    moveList.append(move.clone().setSource(candidateCoordinate))
    def addKingCandidates(moveList, position, move):
        destination = Coordinate.fromAN(move.destination)
        for mx in [1,0,-1]:
            for my in [1,0,-1]:
                if mx != 0 and my != 0:
                    candidateX, candidateY = destination.x+mx, destination.y+my
                else:
                    continue
                if (candidateX >= 8 or candidateX <= 0 or candidateY >= 8 or candidateY <= 0):
                    continue
                candidateCoordinate = Coordinate(candidateX, candidateY)
                if position.pieceAt(candidateCoordinate).upper() == move.pieceType:
                    moveList.append(move.clone().setSource(candidateCoordinate))
    def addQueenCandidates(moveList, position, move):
        MoveVerifier.addBishopCandidates(moveList, position, move)
        MoveVerifier.addRookCandidates(moveList, position, move)
    def addPawnCandidates(moveList, position, move):
        destination = Coordinate.fromAN(move.destination)
      
        candidates = []
        deduceCandidate = lambda movementVector: candidates.append(destination.plus(movementVector))
        if position.gameStatus == GameStatus.WHITE_TO_MOVE:
            if move.isCapture:
                deduceCandidate(Coordinate(-1,-1))
                deduceCandidate(Coordinate( 1,-1))
            else:
                if destination.y == 3:
                    deduceCandidate(Coordinate(0,-2))
                else:
                    deduceCandidate(Coordinate(0,-1))
        elif position.gameStatus == GameStatus.BLACK_TO_MOVE:
            if move.isCapture:
                deduceCandidate(Coordinate(-1,1))
                deduceCandidate(Coordinate( 1,1))
            else:
                if destination.y == 4:
                    deduceCandidate(Coordinate(0,2))
                else:
                    deduceCandidate(Coordinate(0,1))

        for candidate in candidates:
            candidateX = candidate.x
            candidateY = candidate.y

            if (candidateX >= 8 or candidateX <= 0 or candidateY >= 8 or candidateY <= 0):
                continue
            if (position.pieceAt(candidate).upper() == move.pieceType):
                moveList.append(move.clone().setSource(Coordinate(candidateX, candidateY)))

class MoveGenerationError(ValueError):
    def __init__(self, positionFEN, moveAN, errorMessage):
        super().__init__("Error trying to parse position \"%s\" and move %s. %s" % (positionFEN, moveAN, errorMessage))
