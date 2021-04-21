from vector import Vector

class VectorTestSuite:
    def getTests():
        return [
            {"runnable": VectorTestSuite.test1, "name": "Vectors can be instantiated"},
            {"runnable": VectorTestSuite.test2, "name": "Vectors can be instantiated from AN"},
            {"runnable": VectorTestSuite.test3, "name": "Vectors can be equated"},
            {"runnable": VectorTestSuite.test4, "name": "Algebreic Notation has correct values"},
            {"runnable": VectorTestSuite.test5, "name": "Addition of Vectors"},
            {"runnable": VectorTestSuite.test6, "name": "Subtraction of Vectors"}
        ]
    def test1():
        assert(Vector(0,0) != None)
        assert(Vector(1,0) != None)
        assert(Vector(0,1) != None)
        assert(Vector(-1,0) != None)
        assert(Vector(0,-1) != None)
        assert(Vector(-1,-1) != None)
        assert(Vector(1,1) != None)
        return True
    def test2():
        assert (Vector.fromAN("a1") != None)
        assert (Vector.fromAN("h8") != None)
        assert (Vector.fromAN("h2") != None)
        assert (Vector.fromAN("b4") != None)
        return True
    def test3():
        assert(Vector(0,0) == Vector(0,0))
        assert(Vector(1,0) == Vector(1,0))
        assert(Vector(0,2) == Vector(0,2))
        assert(Vector(5,-4) == Vector(5,-4))
        assert(Vector(0,0) != Vector(0,1))
        assert(Vector(1,0) != Vector(1,1))
        assert(Vector(0,2) != Vector(1,2))
        assert(Vector(5,-4) != Vector(5,-3))
        return True
    def test4():
        assert(Vector.fromAN("a1") == Vector(0,0))
        assert(Vector.fromAN("b1") == Vector(1,0))
        assert(Vector.fromAN("a2") == Vector(0,1))
        assert(Vector.fromAN("h8") == Vector(7,7))
        assert(Vector.fromAN("a1") != Vector(1,0))
        assert(Vector.fromAN("b1") != Vector(1,1))
        assert(Vector.fromAN("a2") != Vector(1,1))
        assert(Vector.fromAN("h8") != Vector(7,8))
        return True
    def test5():
        assert(Vector(0,0) + Vector(0,0) == Vector(0,0))
        assert(Vector(1,0) + Vector(0,0) == Vector(1,0))
        assert(Vector(0,1) + Vector(0,0) == Vector(0,1))
        assert(Vector(1,0) + Vector(0,1) == Vector(1,1))
        assert(Vector(3,1) + Vector(-1,-2) == Vector(2,-1))
        assert(Vector(0,0) + Vector(0,0) == Vector.fromAN("a1"))
        assert(Vector.fromAN("a1") + Vector(0,0) == Vector.fromAN("a1"))
        assert(Vector.fromAN("a1") + Vector.fromAN("a1") == Vector.fromAN("a1"))
        assert(Vector.fromAN("b3") + Vector(1, -1) == Vector.fromAN("c2"))
        assert(Vector.fromAN("h8") + Vector(-2,-2) == Vector.fromAN("f6"))
        assert(Vector.fromAN("b2") + Vector.fromAN("b2") == Vector(2,2))
        assert(
            sum([
                Vector.fromAN("b2"),
                Vector.fromAN("b2"),
                Vector.fromAN("b2")
            ]) == Vector.fromAN("d4"))
        return True
    def test6():
        assert(Vector(0,0) - Vector(0,0) == Vector(0,0))
        assert(Vector(4,0) - Vector(1,0) == Vector(3,0))
        assert(Vector(0,4) - Vector(0,1) == Vector(0,3))
        assert(Vector(4,4) - Vector(1,1) == Vector(3,3))
        assert(Vector(0,0) - Vector(1,2) == Vector(-1,-2))
        assert(Vector.fromAN("a1") - Vector.fromAN("a1") == Vector.fromAN("a1"))
        assert(Vector.fromAN("c2") - Vector.fromAN("b3") == Vector(1,-1))
        return True
