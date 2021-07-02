from __future__ import annotations
from typing import List, Union
from .move_generator import MoveGenerator
from .constraints import Constraints
from .position import Position
from .move import Move, UnfinishedMove
from .castling_move import CastlingMove


class MoveVerifier():
    @staticmethod
    def verifyGame(position: Position, moveList: List[UnfinishedMove]) -> ConstraintResult:
        currentPosition = position
        for move in moveList:
            result = MoveVerifier.verifyMove(currentPosition, move)
            if not result.isLegal: 
                break
            currentPosition = result.updatedPosition
        return result

    @staticmethod
    def verifyMove(position: Position, move: UnfinishedMove) -> ConstraintResult:
        constrainedMoves: List[ConstraintResult] = [] #TODO: SMELL - Misrepresentative Name
        for candidate in MoveGenerator.generateMoveList(position, move):
            constrainedMoves.append(
                MoveVerifier.verifyCandidate(position, candidate)
            )
        legalMoves: List[ConstraintResult] = [m for m in constrainedMoves if m.isLegal] #TODO: SMELL - Misrepresentative Name
        if len(legalMoves) == 0 and len(constrainedMoves) == 1:
            return ConstraintResult.fail(
                    "Illegal Move: The move %s is illegal because %s"
                    % (move, constrainedMoves[0].reason),
                position, move)
        elif len(legalMoves) == 0: 
            return ConstraintResult.fail(
                    "No Legal Moves: The move %s is illegal because %s"
                    % (move, [result.reason for result in constrainedMoves]),
                position, move)
        elif len(legalMoves) > 1:
            return ConstraintResult.fail(
                    "Ambiguous Move: The move %s leads to multiple valid moves [%s]"
                    % (move, list(map(lambda m: m.move, legalMoves))),
                position, move)
        elif len(legalMoves) == 1:
            validMove = legalMoves[0] #TODO: SMELL - Mysterious Name
            return ConstraintResult.accept(validMove.updatedPosition, validMove.move) 
        else:
            raise NotImplementedError("Impossible Code")
    
    @staticmethod
    def verifyCandidate(position: Position, move: Move) -> ConstraintResult:
        for constraint in Constraints.getPreMoveConstraints():
            result = constraint(position, move)
            if not result.isLegal:
                return ConstraintResult.fail(result.reason, position, move)

        if isinstance(move, CastlingMove):
            halfPosition = position.halfCastle(move)
            for constraint in Constraints.getMidCastleConstraints():
                result = constraint(position, move)
                if not result.isLegal:
                    return ConstraintResult.fail(result.reason, position, move)
            newPosition = halfPosition.finishCastle(move)
        else:
            newPosition = position.next(move)

        for constraint in Constraints.getPostMoveConstraints():
            result = constraint(newPosition, move)
            if not result.isLegal:
                return ConstraintResult.fail(result.reason, newPosition, move)
        return ConstraintResult.accept(newPosition, move)


class ConstraintResult():
    def __init__(self, reason: str, updatedPosition: Position, move: Union[UnfinishedMove | Move], isLegal: bool):
        self.reason = reason
        self.updatedPosition = updatedPosition
        self.move = move
        self.isLegal = isLegal

    @staticmethod
    def accept(position: Position, move: Union[UnfinishedMove | Move]) -> ConstraintResult:
        return ConstraintResult("", position, move, True)

    @staticmethod
    def fail(reason: str, position: Position, move: Union[UnfinishedMove | Move]) -> ConstraintResult:
        assert(isinstance(reason, str))
        return ConstraintResult(reason, position, move, False)