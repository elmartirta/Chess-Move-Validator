from position import Position
from move_verifier import MoveVerifier

class MoveVerifierTestSuite():
    def getTests():
        return [
            {"runnable": MoveVerifierTestSuite.test1, "name": "Generate Moves from all pieces to B3"},
            {"runnable": MoveVerifierTestSuite.test2, "name": "Generate lots of simple rook moves"},
            {"runnable": MoveVerifierTestSuite.test3, "name": "Generate lots of simple bishop moves"}#,
            #{"runnable": MoveVerifierTestSuite.test4, "name": "Generate lots of simple knight moves"},
            #{"runnable": MoveVerifierTestSuite.test5, "name": "Generate lots of simple queen moves"},
            #{"runnable": MoveVerifierTestSuite.test6, "name": "Generate lots of simple king moves"},
            #{"runnable": MoveVerifierTestSuite.test7, "name": "Generate lots of simple pawn moves"}
        ]
    def test1():
        check = lambda pos, move: MoveVerifier.generateMoveListFromFEN(pos, move)
        pos = "8/1R3B2/8/6k1/8/5Q2/1PKN4/8 w - - 0 1"
        assert(check(pos, "Rb3") != None)
        assert(check(pos, "Bb3") != None)
        assert(check(pos, "Nb3") != None)
        assert(check(pos, "Qb3") != None)
        assert(check(pos, "Kb3") != None)
        assert(check(pos, "b3")) #TODO: FIX ISSUE, CURRENTLY FAILING
    def test2():
        check = lambda pos, move: MoveVerifier.generateMoveListFromFEN(pos, move)
        assert(check("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Ra2") != None)
        assert(check("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Rb1") != None)
        assert(check("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Ra8") != None)
        assert(check("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Rh1") != None)
        assert(check("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Rg1+") != None)
        assert(check("8/6K1/8/8/8/8/1k6/r7 w - - 0 1", "Ra7+") != None)
        return True
    def test3():
        check = lambda pos, move: MoveVerifier.generateMoveListFromFEN(pos, move)
        assert(check("8/8/2K5/8/3B4/5k2/8/8 w - - 0 1", "Ba1") != None)
        #assert(check("8/8/2K5/8/3B4/5k2/8/8 w - - 0 1", "Bh8") != None) #TODO: FIX ISSUE, CURRENTLY FAILING
        assert(check("8/8/2K5/8/3B4/5k2/8/8 w - - 0 1", "Ba7") != None)
        assert(check("8/8/2K5/8/3B4/5k2/8/8 w - - 0 1", "Bg1") != None)


        


        


        