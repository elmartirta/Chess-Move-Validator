from vector2D import Vector2D

class Vector2DTestSuite:
    def getTests():
        return [
            {"runnable": Vector2DTestSuite.test1, "name": "Vectors can be instantiated"},
            {"runnable": Vector2DTestSuite.test2, "name": "Vectors can be instantiated from AN"},
            {"runnable": Vector2DTestSuite.test3, "name": "Vectors can be equated"},
            {"runnable": Vector2DTestSuite.test4, "name": "Algebreic Notation has correct values"},
            {"runnable": Vector2DTestSuite.test5, "name": "Addition of Vectors"},
            {"runnable": Vector2DTestSuite.test6, "name": "Subtraction of Vectors"}
        ]
    def test1():
        assert(Vector2D(0,0) != None)
        assert(Vector2D(1,0) != None)
        assert(Vector2D(0,1) != None)
        assert(Vector2D(-1,0) != None)
        assert(Vector2D(0,-1) != None)
        assert(Vector2D(-1,-1) != None)
        assert(Vector2D(1,1) != None)
        return True
    def test2():
        assert (Vector2D.fromAN("a1") != None)
        assert (Vector2D.fromAN("h8") != None)
        assert (Vector2D.fromAN("h2") != None)
        assert (Vector2D.fromAN("b4") != None)
        return True
    def test3():
        assert(Vector2D(0,0) == Vector2D(0,0))
        assert(Vector2D(1,0) == Vector2D(1,0))
        assert(Vector2D(0,2) == Vector2D(0,2))
        assert(Vector2D(5,-4) == Vector2D(5,-4))
        assert(Vector2D(0,0) != Vector2D(0,1))
        assert(Vector2D(1,0) != Vector2D(1,1))
        assert(Vector2D(0,2) != Vector2D(1,2))
        assert(Vector2D(5,-4) != Vector2D(5,-3))
        return True
    def test4():
        assert(Vector2D.fromAN("a1") == Vector2D(0,0))
        assert(Vector2D.fromAN("b1") == Vector2D(1,0))
        assert(Vector2D.fromAN("a2") == Vector2D(0,1))
        assert(Vector2D.fromAN("h8") == Vector2D(7,7))
        assert(Vector2D.fromAN("a1") != Vector2D(1,0))
        assert(Vector2D.fromAN("b1") != Vector2D(1,1))
        assert(Vector2D.fromAN("a2") != Vector2D(1,1))
        assert(Vector2D.fromAN("h8") != Vector2D(7,8))
        return True
    def test5():
        assert(Vector2D(0,0) + Vector2D(0,0) == Vector2D(0,0))
        assert(Vector2D(1,0) + Vector2D(0,0) == Vector2D(1,0))
        assert(Vector2D(0,1) + Vector2D(0,0) == Vector2D(0,1))
        assert(Vector2D(1,0) + Vector2D(0,1) == Vector2D(1,1))
        assert(Vector2D(3,1) + Vector2D(-1,-2) == Vector2D(2,-1))
        assert(Vector2D(0,0) + Vector2D(0,0) == Vector2D.fromAN("a1"))
        assert(Vector2D.fromAN("a1") + Vector2D(0,0) == Vector2D.fromAN("a1"))
        assert(Vector2D.fromAN("a1") + Vector2D.fromAN("a1") == Vector2D.fromAN("a1"))
        assert(Vector2D.fromAN("b3") + Vector2D(1, -1) == Vector2D.fromAN("c2"))
        assert(Vector2D.fromAN("h8") + Vector2D(-2,-2) == Vector2D.fromAN("f6"))
        assert(Vector2D.fromAN("b2") + Vector2D.fromAN("b2") == Vector2D(2,2))
        assert(sum([Vector2D.fromAN("b2"),Vector2D.fromAN("b2"),Vector2D.fromAN("b2")]) == Vector2D.fromAN("d4"))
        return True
    def test6():
        assert(Vector2D(0,0) - Vector2D(0,0) == Vector2D(0,0))
        assert(Vector2D(4,0) - Vector2D(1,0) == Vector2D(3,0))
        assert(Vector2D(0,4) - Vector2D(0,1) == Vector2D(0,3))
        assert(Vector2D(4,4) - Vector2D(1,1) == Vector2D(3,3))
        assert(Vector2D(0,0) - Vector2D(1,2) == Vector2D(-1,-2))
        assert(Vector2D.fromAN("a1") - Vector2D.fromAN("a1") == Vector2D.fromAN("a1"))
        assert(Vector2D.fromAN("c2") - Vector2D.fromAN("b3") == Vector2D(1,-1))
        return True
