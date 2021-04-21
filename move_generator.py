from position import Position
from move import Move
from vector import Vector 
from castling_move import CastlingMove

class MoveGenerator():
    def generateMoveListFromFEN(positionFEN, moveAN):
        return MoveGenerator.generateMoveList(Position.fromFEN(positionFEN), CastlingMove.fromAN(moveAN))
    def generateMoveList(position, move):
        moveList = []
        if move.pieceType == None: 
            raise MoveGenerationError(positionFEN, moveAN, "PieceType is None")
        if isinstance(move, CastlingMove): MoveGenerator.addCastlingCandidates(moveList, position, move)
        elif (move.pieceType in "rR"): MoveGenerator.addRookCandidates(moveList, position, move)
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
                if position.pieceTypeIs(candidate, move.pieceType):
                    moveList.append(move.clone().setSource(candidate))
    def addBishopCandidates(moveList, position, move):
        for i in range(1,10):
            for delta in [
                    Vector( i, i),
                    Vector(-i, i),
                    Vector( i,-i),
                    Vector(-i,-i)]:
                candidate = move.destination + delta
                if candidate.isInsideChessboard() and position.pieceTypeIs(candidate, move.pieceType):
                    moveList.append(move.clone().setSource(candidate))
    def addKnightCandidates(moveList, position, move):
        for n in [Vector(1,2), Vector(2,1)]:
            for delta in [
                    Vector( n.x, n.y),
                    Vector(-n.x, n.y),
                    Vector( n.x,-n.y),
                    Vector(-n.x,-n.y)]:
                candidate = move.destination + delta
                if candidate.isInsideChessboard() and position.pieceTypeIs(candidate, move.pieceType):
                    moveList.append(move.clone().setSource(candidate))
    def addKingCandidates(moveList, position, move):
        for dx in [1,0,-1]:
            for dy in [1,0,-1]:
                if dx == 0 and dy == 0: continue
                delta = Vector(dx, dy)
                candidate = move.destination + delta
                if candidate.isInsideChessboard() and position.pieceTypeIs(candidate, move.pieceType):
                    moveList.append(move.clone().setSource(candidate))
    def addQueenCandidates(moveList, position, move):
        MoveGenerator.addBishopCandidates(moveList, position, move)
        MoveGenerator.addRookCandidates(moveList, position, move)
    def addPawnCandidates(moveList, position, move):
        destination = move.destination
      
        deltas = []
        dy = -1 if position.isWhiteToMove() else 1
        if move.isCapture:
            deltas.append(Vector(-1,dy))
            deltas.append(Vector( 1,dy))
        else:
            deltas.append(Vector(0,dy))
            if (destination.y == 3 and position.isWhiteToMove()) or \
                    (destination.y == 4 and not position.isWhiteToMove()):
                deltas.append(Vector(0,2*dy))

        for delta in deltas:
            candidate = move.destination + delta
            if candidate.isInsideChessboard() and position.pieceTypeIs(candidate, move.pieceType):
                moveList.append(move.clone().setSource(candidate))
    def addCastlingCandidates(moveList, position, move):
        homeIndex = 0 if position.isWhiteToMove() else 7
        homeRow = [Vector(x, homeIndex) for x in range(0,8)]
        homeRow = [position.pieceTypeOf(tile) for tile in homeRow]
        kingSymbol = "K" if position.isWhiteToMove() else "k"
        king = Vector.fromNonExistent()
        if not kingSymbol in homeRow:
            king = None
        else:
            rook = None
            kingPos = homeRow.index(kingSymbol)
            king = Vector(kingPos, homeIndex)
            edge = Vector(7, homeIndex) if move.isKingsideCastling() else Vector(0, homeIndex)
            for rookCandidate in king.between(edge) + [edge]:
                if position.pieceTypeOf(rookCandidate) == "R" \
                        and position.pieceIsWhite(rookCandidate) == (position.isWhiteToMove()):
                    rook = rookCandidate
                    break        
        output = move.clone()
        output.source = king
        output.destination = king + (Vector(2,0) if move.isKingsideCastling() else Vector(-2, 0))
        output.rookLocation = rook
        return moveList.append(output)

class MoveGenerationError(ValueError):
    def __init__(self, positionFEN, moveAN, errorMessage):
        #TODO: SMELL - Line Length
        super().__init__("Error trying to parse position \"%s\" and move %s. %s" % (positionFEN, moveAN, errorMessage))
