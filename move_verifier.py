from __future__ import annotations
from typing import List
from move_generator import MoveGenerator
from move_filter import MoveFilter
from position import Position
from move import Move
from castling_move import CastlingMove
import enum


class MoveVerifier():
    @staticmethod
    def verifyGame(position: Position, moveList: List[Move]) -> VerificationResult:
        currentPosition = position
        for move in moveList:
            result = MoveVerifier.verifyMove(currentPosition, move)
            if not result.isLegal: 
                break
            currentPosition = result.updatedPosition
        return result

    @staticmethod
    def verifyMoveFromFEN(positionFEN: str, moveAN: str) -> VerificationResult:
        return MoveVerifier.verifyMove(
            Position.fromFEN(positionFEN), 
            Move.fromAN(moveAN))

    @staticmethod
    def verifyMove(position: Position, move: Move) -> VerificationResult:
        filteredMoves: List[VerificationResult] = [] #TODO: SMELL - Misrepresentative Name
        for candidate in MoveGenerator.generateMoveList(position, move):
            filteredMoves.append(
                MoveVerifier.verifyCandidate(position, candidate)
            )
        legalMoves: List[VerificationResult] = [m for m in filteredMoves if m.isLegal] #TODO: SMELL - Misrepresentative Name
        if len(legalMoves) == 0 and len(filteredMoves) == 1:
            return VerificationResult.fail(
                    "Illegal Move: The move %s is illegal because %s"
                    % (move, filteredMoves[0].reason),
                position, move)
        elif len(legalMoves) == 0: 
            return VerificationResult.fail(
                    "No Legal Moves: The move %s is illegal because %s"
                    % (move, [result.reason for result in filteredMoves]),
                position, move)
        elif len(legalMoves) > 1:

            return VerificationResult.fail(
                    "Ambiguous Move: The move %s leads to multiple valid moves [%s]"
                    % (move, legalMoves),
                position, move)
        elif len(legalMoves) == 1:
            validMove = legalMoves[0] #TODO: SMELL - Mysterious Name
            return VerificationResult.accept(validMove.updatedPosition, validMove.move) 
        else:
            raise NotImplementedError("Impossible Code")
    
    @staticmethod
    def verifyCandidate(position: Position, move: Move) -> VerificationResult:
        def checkAllFilters(filters, position, move):
            for moveFilter in filters:
                filterResult = moveFilter(position, move)
                if not filterResult.isLegal:
                    return VerificationResult.fail(filterResult.reason, position, move)

        checkAllFilters(MoveFilter.getPreMoveFilters(), position, move)

        if isinstance(move, CastlingMove):
            halfPosition = position.halfCastle(move)
            checkAllFilters(MoveFilter.getMidCastleFilters(), position, move)
            newPosition = halfPosition.finishCastle(move)
        else:
            newPosition = position.next(move)

        for moveFilter in MoveFilter.getPostMoveFilters():
            filterResult = moveFilter(newPosition, move)
            if not filterResult.isLegal:
                return VerificationResult.fail(filterResult.reason, newPosition, move)

        return VerificationResult.accept(newPosition, move)


class VerificationResult():
    def __init__(self, reason: str, updatedPosition: Position, move: Move, isLegal: bool):
        self.reason = reason
        self.updatedPosition = updatedPosition
        self.move = move
        self.isLegal = isLegal

    @staticmethod
    def accept(position: Position, move: Move) -> VerificationResult:
        return VerificationResult("", position, move, True)

    @staticmethod
    def fail(reason: str, position: Position, move: Move) -> VerificationResult:
        assert(isinstance(reason, str))
        return VerificationResult(reason, position, move, False)