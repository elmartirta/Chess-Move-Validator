from notation_parser import NotationParser
from typing import List
from position import Position
from move import Move
from vector import Vector 
from castling_move import CastlingMove


class MoveGenerator():
    @staticmethod
    def generateMoveListFromFEN(positionFEN: str, moveAN: str) -> List[Move]:
        return MoveGenerator.generateMoveList(
            NotationParser.parsePosition(positionFEN),
            NotationParser.parseAlgebreicNotation(moveAN)
        )

    @staticmethod
    def generateMoveList(position: Position, move: Move) -> List[Move]:
        moveList: List[Move] = []
        if move.pieceType == None: 
            raise MoveGenerationError(position, move, "PieceType is None")
        if isinstance(move, CastlingMove): MoveGenerator.addCastlingCandidates(moveList, position, move)
        elif (move.pieceType in "rR"): MoveGenerator.addRookCandidates(moveList, position, move)
        elif (move.pieceType in "bB"): MoveGenerator.addBishopCandidates(moveList, position, move)
        elif (move.pieceType in "qQ"): MoveGenerator.addQueenCandidates(moveList, position, move)
        elif (move.pieceType in "nN"): MoveGenerator.addKnightCandidates(moveList, position, move)
        elif (move.pieceType in "kK"): MoveGenerator.addKingCandidates(moveList, position, move)
        elif (move.pieceType in "pP"): MoveGenerator.addPawnCandidates(moveList, position, move)
        else:
            raise MoveGenerationError(position, move, "Unsupported Piece type: " + move.pieceType)
        return moveList
    
    @staticmethod
    def addRookCandidates(moveList: List[Move], position: Position, move: Move) -> None:
        if move.destination is None: raise ValueError() #TODO: SMELL - Lazy Error Writing
        rookLocations = position.getOrthogonalsTargeting(move.destination)
        for candidate in rookLocations:
            if candidate == move.destination: 
                continue
            if position.pieceTypeIs(candidate, move.pieceType):
                moveList.append(move.clone().setSource(candidate))
    
    @staticmethod
    def addBishopCandidates(moveList: List[Move], position: Position, move: Move) -> None:
        if move.destination is None: raise ValueError() #TODO: SMELL - Lazy Error Writing
        bishopLocations = position.getDiagonalsTargeting(move.destination)
        for candidate in bishopLocations:
            if position.pieceTypeIs(candidate, move.pieceType):
                moveList.append(move.clone().setSource(candidate))
    
    @staticmethod
    def addKnightCandidates(moveList: List[Move], position: Position, move: Move) -> None:
        if move.destination is None: raise ValueError() #TODO: SMELL - Lazy Error Writing
        for candidate in position.getKnightSquaresTargeting(move.destination):
            if position.pieceTypeIs(candidate, move.pieceType):
                moveList.append(move.clone().setSource(candidate))
    
    @staticmethod
    def addKingCandidates(moveList: List[Move], position: Position, move: Move) -> None:
        if move.destination is None: raise ValueError() #TODO: SMELL - Lazy Error Writing
        for candidate in position.getKingsTargeting(move.destination):
            if candidate.isInsideChessboard() and position.pieceTypeIs(candidate, move.pieceType):
                moveList.append(move.clone().setSource(candidate))
    
    @staticmethod
    def addQueenCandidates(moveList: List[Move], position: Position, move: Move) -> None:
        MoveGenerator.addBishopCandidates(moveList, position, move)
        MoveGenerator.addRookCandidates(moveList, position, move)

    @staticmethod
    def addPawnCandidates(moveList: List[Move], position: Position, move: Move) -> None:
        if move.destination is None: raise ValueError() #TODO: SMELL - Lazy Error Writing
        destination = move.destination
      
        deltas = []
        dy = -1 if position.isWhiteToMove else 1
        if move.isCapture:
            deltas.append(Vector(-1,dy))
            deltas.append(Vector( 1,dy))
        else:
            deltas.append(Vector(0,dy))
            if (destination.y == 3 and position.isWhiteToMove) or \
                    (destination.y == 4 and not position.isWhiteToMove):
                deltas.append(Vector(0,2*dy))

        for delta in deltas:
            candidate = move.destination + delta
            if candidate.isInsideChessboard() and position.pieceTypeIs(candidate, move.pieceType):
                moveList.append(move.clone().setSource(candidate))

    @staticmethod
    def addCastlingCandidates(moveList: List[Move], position: Position, move: CastlingMove) -> None:
        homeIndex = 0 if position.isWhiteToMove else 7
        homeRow_temp = [Vector(x, homeIndex) for x in range(0,8)]
        homeRow = [position.pieceTypeOf(tile) for tile in homeRow_temp]
        kingSymbol = "K" if position.isWhiteToMove else "k"
        king = None
        if not kingSymbol in homeRow:
            king = None
        else:
            rook = None
            kingPos = homeRow.index(kingSymbol)
            king = Vector(kingPos, homeIndex)
            edge = Vector(7, homeIndex) if move.isKingsideCastling() else Vector(0, homeIndex)
            for rookCandidate in king.between(edge) + [edge]:
                if position.pieceTypeOf(rookCandidate) == "R" \
                        and position.pieceIsWhite(rookCandidate) == (position.isWhiteToMove):
                    rook = rookCandidate
                    break        
        output = move.clone()
        if king is None: raise ValueError() #TODO - Lazy Error Writing
        output.source = king
        output.destination = king + (Vector(2,0) if move.isKingsideCastling() else Vector(-2, 0))
        output.rookLocation = rook
        return moveList.append(output)


class MoveGenerationError(ValueError):
    def __init__(self, positionFEN, moveAN, errorMessage):
        super().__init__(
            "Error trying to parse position \"%s\" and move %s. %s" 
            % (positionFEN, moveAN, errorMessage))
