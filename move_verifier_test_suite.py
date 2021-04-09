from move_verifier import MoveVerifier
from position import Position
from move import Move
class MoveVerifierTestSuite():
    def getTests():
        return [
            {"runnable": MoveVerifierTestSuite.test1, "name": "Just. 1. e4."},
            {"runnable": MoveVerifierTestSuite.test2, "name": "Just. 1. e4 e5"},
            {"runnable": MoveVerifierTestSuite.test3, "name": "JUST DOUBLE BONGCLOUD (Carleson vs Nakamura 2021)"}
        ]
    def test(position, move):
        res = MoveVerifier.verifyGame(position, move)
        if res.isLegal: 
            return True
        else:
            print(res.reason)
            return False
    def test1():
        return MoveVerifierTestSuite.test(Position.fromStartingPosition(), [
            Move.fromAN("e4")
        ])
    def test2():
        return MoveVerifierTestSuite.test(Position.fromStartingPosition(), [
            Move.fromAN("e4"),
            Move.fromAN("e5"),
        ])
    def test3():
        return MoveVerifierTestSuite.test(Position.fromStartingPosition(), [
            Move.fromAN("e4"),
            Move.fromAN("e5"),
            Move.fromAN("Ke2"),
            Move.fromAN("Ke7"),
            Move.fromAN("Ke1"),
            Move.fromAN("Ke8"),
            Move.fromAN("Ke2"),
            Move.fromAN("Ke7"),
            Move.fromAN("Ke1"),
            Move.fromAN("Ke8")
        ])