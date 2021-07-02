
from .notation_parser import NotationParser
from typing import List
from .position import Position
from .move import Move, UnfinishedMove
from .vector import Vector 
from .castling_move import UnfinishedCastlingMove


class MoveGenerator():
    @classmethod
    def generateMoveListFromStartingPosition(cls, moveAN: str) -> List[Move]:
        return cls.generateMoveList(
            NotationParser.fromStartingPosition(),
            NotationParser.parseAlgebreicNotation(moveAN)
        )

    @classmethod
    def generateMoveListFromFEN(cls, positionFEN: str, moveAN: str) -> List[Move]:
        return cls.generateMoveList(
            NotationParser.parsePosition(positionFEN),
            NotationParser.parseAlgebreicNotation(moveAN)
        )

    @classmethod
    def generateMoveList(cls, position: Position, move: UnfinishedMove) -> List[Move]:
        moveList: List[Move] = []
        if move.pieceType == None: 
            raise MoveGenerationError(position, move, "PieceType is None")
    
        if isinstance(move, UnfinishedCastlingMove): 
            cls._addCastlingCandidates(moveList, position, move)
        else: 
            board = position.board
            candidates: List[Vector] = []
            if move.destination is None:
                raise ValueError(f"There is no destination for the move: {move}")
            destination = move.destination
            if   (move.pieceType in "rR"): candidates = board.getRooksAttacking(destination)
            elif (move.pieceType in "bB"): candidates = board.getBishopsAttacking(destination)
            elif (move.pieceType in "qQ"): candidates = board.getQueensAttacking(destination)
            elif (move.pieceType in "nN"): candidates = board.getKnightsAttacking(destination)
            elif (move.pieceType in "kK"): candidates = board.getKingsTargeting(destination)
            elif (move.pieceType in "pP"): candidates = cls._addPawnCandidates(moveList, position, move)
            else:
                raise MoveGenerationError(position, move, f"Unsupported Piece type: {move.pieceType}")

            for candidate in candidates:
                if candidate == move.destination: 
                    continue
                if board.pieceTypeIs(candidate, move.pieceType):
                    moveList.append(move.complete(candidate, destination))
        
        return moveList
    

    @staticmethod
    def _addPawnCandidates(moveList: List[Move], position: Position, move: UnfinishedMove) -> List[Vector]:
        if move.destination is None: raise ValueError() #TODO: Lazy Error Writing
        if move.isCapture:
            pawnCandidates = position.board.getPawnsAttacking(move.destination)
        else:
            pawnCandidates = position.board.getPawnsWalkingTo(move.destination)

        return pawnCandidates

    @staticmethod
    def _addCastlingCandidates(moveList: List[Move], position: Position, move: UnfinishedCastlingMove) -> None:
        homeIndex = 0 if position.isWhiteToMove else 7
        homeRow_temp = [Vector(x, homeIndex) for x in range(0,8)]
        homeRow = [position.board.pieceTypeOf(tile) for tile in homeRow_temp]
        kingSymbol = "K" if position.isWhiteToMove else "k"
        king = None
        if not kingSymbol in homeRow:
            king = None
        else:
            rook = None
            kingPos = homeRow.index(kingSymbol)
            king = Vector(kingPos, homeIndex)
            edge = Vector(7, homeIndex) if move.isKingsideCastling else Vector(0, homeIndex)
            for rookCandidate in king.between(edge) + [edge]:
                if position.board.pieceTypeOf(rookCandidate) == "R" \
                        and position.board.pieceIsWhite(rookCandidate) == (position.isWhiteToMove):
                    rook = rookCandidate
                    break        
        output = move.clone()
        if king is None: raise ValueError() #TODO - Lazy Error Writing
        source = king
        destination = king + (Vector(2,0) if move.isKingsideCastling else Vector(-2, 0))
        rookLocation = rook
        moveList.append(output.complete(source, destination, rookLocation))


class MoveGenerationError(ValueError):
    def __init__(self, positionFEN, moveAN, errorMessage):
        super().__init__(
            f"Error trying to parse position \"{positionFEN}\" and move {moveAN}. {errorMessage}")
