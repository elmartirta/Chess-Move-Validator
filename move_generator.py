from board import Board
from notation_parser import NotationParser
from typing import List, Union
from position import Position
from move import Move
from vector import Vector 
from castling_move import CastlingMove


class MoveGenerator():
    @classmethod
    def generateMoveListFromFEN(cls, positionFEN: str, moveAN: str) -> List[Move]:
        return cls.generateMoveList(
            NotationParser.parsePosition(positionFEN),
            NotationParser.parseAlgebreicNotation(moveAN)
        )

    @classmethod
    def generateMoveList(cls, position: Position, move: Union[Move, CastlingMove]) -> List[Move]:
        moveList: List[Move] = []
        if move.pieceType == None: 
            raise MoveGenerationError(position, move, "PieceType is None")
        board = position.board
    
        candidates: List[Vector] = []
        if isinstance(move, CastlingMove): 
            cls._addCastlingCandidates(moveList, position, move)
        else: 
            if move.destination is None:
                raise ValueError("There is no destination for the move: " + str(move))
            destination = move.destination
            if (move.pieceType in "rR"): 
                candidates = board.getOrthogonalsTargeting(destination)
            elif (move.pieceType in "bB"): 
                candidates = board.getDiagonalsTargeting(destination)
            elif (move.pieceType in "qQ"): 
                candidates =  board.getOrthogonalsTargeting(destination)
                candidates += board.getDiagonalsTargeting(destination)
            elif (move.pieceType in "nN"): 
                candidates = board.getKnightSquaresTargeting(destination)
            elif (move.pieceType in "kK"): 
                candidates = board.getKingsTargeting(destination)
            elif (move.pieceType in "pP"): 
                candidates = cls._addPawnCandidates(moveList, position, move)
            else:
                raise MoveGenerationError(position, move, "Unsupported Piece type: " + move.pieceType)

        for candidate in candidates:
            if candidate == move.destination: 
                continue
            if board.pieceTypeIs(candidate, move.pieceType):
                moveList.append(move.clone().setSource(candidate))
        
        return moveList
    

    @staticmethod
    def _addPawnCandidates(moveList: List[Move], position: Position, move: Move) -> List[Vector]:
        if move.destination is None: raise ValueError() #TODO: Lazy Error Writing
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

        pawnCandidates: List[Vector] = []
        for delta in deltas:
            candidate = move.destination + delta
            pawnCandidates += [candidate]
        return pawnCandidates

    @staticmethod
    def _addCastlingCandidates(moveList: List[Move], position: Position, move: CastlingMove) -> None:
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
        output.source = king
        output.destination = king + (Vector(2,0) if move.isKingsideCastling else Vector(-2, 0))
        output.rookLocation = rook
        moveList.append(output)


class MoveGenerationError(ValueError):
    def __init__(self, positionFEN, moveAN, errorMessage):
        super().__init__(
            "Error trying to parse position \"%s\" and move %s. %s" 
            % (positionFEN, moveAN, errorMessage))
