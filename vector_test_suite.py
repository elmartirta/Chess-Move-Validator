from vector import Vector


class VectorTestSuite:
    @staticmethod
    def getTests():
        return [
            {"runnable": VectorTestSuite.vecInit, "name": "Vectors can be instantiated"},
            {"runnable": VectorTestSuite.vecInitAN, "name": "Vectors can be instantiated from AN"},
            {"runnable": VectorTestSuite.vecEq, "name": "Vectors can be equated"},
            {"runnable": VectorTestSuite.anValid, "name": "Algebreic Notation has correct values"},
            {"runnable": VectorTestSuite.vecAdd, "name": "Addition of Vectors"},
            {"runnable": VectorTestSuite.vecSub, "name": "Subtraction of Vectors"}
        ]

    @staticmethod
    def vecInit():
        assert(Vector(0,0) != None)
        assert(Vector(1,0) != None)
        assert(Vector(0,1) != None)
        assert(Vector(-1,0) != None)
        assert(Vector(0,-1) != None)
        assert(Vector(-1,-1) != None)
        assert(Vector(1,1) != None)
        return True
    
    @staticmethod
    def vecInitAN():
        assert (Vector.fromAN("a1") != None)
        assert (Vector.fromAN("h8") != None)
        assert (Vector.fromAN("h2") != None)
        assert (Vector.fromAN("b4") != None)
        return True
    
    @staticmethod
    def vecEq():
        assert(Vector(0,0) == Vector(0,0))
        assert(Vector(1,0) == Vector(1,0))
        assert(Vector(0,2) == Vector(0,2))
        assert(Vector(5,-4) == Vector(5,-4))
        assert(Vector(0,0) != Vector(0,1))
        assert(Vector(1,0) != Vector(1,1))
        assert(Vector(0,2) != Vector(1,2))
        assert(Vector(5,-4) != Vector(5,-3))
        return True
    
    @staticmethod
    def anValid():
        assert(Vector.fromAN("a1") == Vector(0,0))
        assert(Vector.fromAN("b1") == Vector(1,0))
        assert(Vector.fromAN("a2") == Vector(0,1))
        assert(Vector.fromAN("h8") == Vector(7,7))
        assert(Vector.fromAN("a1") != Vector(1,0))
        assert(Vector.fromAN("b1") != Vector(1,1))
        assert(Vector.fromAN("a2") != Vector(1,1))
        assert(Vector.fromAN("h8") != Vector(7,8))
        return True
    
    @staticmethod
    def vecAdd():
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
    
    @staticmethod
    def vecSub():
        assert(Vector(0,0) - Vector(0,0) == Vector(0,0))
        assert(Vector(4,0) - Vector(1,0) == Vector(3,0))
        assert(Vector(0,4) - Vector(0,1) == Vector(0,3))
        assert(Vector(4,4) - Vector(1,1) == Vector(3,3))
        assert(Vector(0,0) - Vector(1,2) == Vector(-1,-2))
        assert(Vector.fromAN("a1") - Vector.fromAN("a1") == Vector.fromAN("a1"))
        assert(Vector.fromAN("c2") - Vector.fromAN("b3") == Vector(1,-1))
        return True