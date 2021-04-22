from move_generator import MoveGenerator
from move_filter import MoveFilter
from position import Position
from move import Move
from castling_move import CastlingMove
import enum


class MoveVerifier():
    def verifyGame(position, moveList):
        currentPosition = position
        for move in moveList:
            result = MoveVerifier.verifyMove(currentPosition, move)
            if not result.isLegal: 
                break
            currentPosition = result.updatedPosition
        return result

    def verifyMoveFromFEN(positionFEN, moveAN):
        return MoveVerifier.verifyMove(Position.fromFEN(positionFEN), Move.fromAN(moveAN))

    def verifyMove(position, move):
        candidates = MoveGenerator.generateMoveList(position, move)
        results = []
        for candidate in candidates:
            finalResult = MoveVerifier.verifyCandidate(position, candidate)
            results.append(finalResult)
        legalMoves = [result for result in results if result.isLegal == True]
        if len(legalMoves) == 0:
            if (len(results) == 1):
                assert(isinstance(results[0].reason, str))
                return VerificationResult.fail(
                        "Illegal Move: The move %s is illegal because %s"
                        % (move, results[0].reason),
                   position, move)
            else: 
                return VerificationResult.fail(
                        "No Legal Moves: The move %s is illegal because %s"
                        % (move, [result.reason for result in results]),
                    position, move)
        elif len(legalMoves) == 1:
            validMove = legalMoves[0]
            return VerificationResult.accept(validMove.updatedPosition, validMove)
        else:
            return VerificationResult.fail(
                    "Ambiguous Move: The move %s leads to multiple valid moves [%s]"
                    % (move, legalMoves),
                position, move)
    
    def verifyCandidate(position, move):
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
    def __init__(self, reason, updatedPosition, move, isLegal):
        self.reason = reason
        self.updatedPosition = updatedPosition
        self.move = move
        self.isLegal = isLegal

    def accept(position, move):
        return VerificationResult("", position, move, True)

    def fail(reason, position, move):
        assert(isinstance(reason, str))
        return VerificationResult(reason, position, move, False)