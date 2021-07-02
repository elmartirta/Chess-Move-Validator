from typing import List
from verifier.vector import Vector
from verifier.board import Board


class BoardTestSuite():
    @classmethod
    def getTests(cls):
        return[
            {"runnable": cls.initializeEmptyBoard, "name": "Initialize a Board object"},
            {"runnable": cls.boardHasSquares, "name": "Board() contains an 8x8 .squares matrix"},
            {"runnable": cls.emptyBoardFromFen, "name": "Initialize a Board object"},
            {"runnable": cls.startingBoardFromFEN, "name": "Initialize a Board object"},
            {"runnable": cls.boardEquality, "name": "Is able to compare boards"},
            {"runnable": cls.canSee, "name": "Checking if pieces can see others"},
            {"runnable": cls.rooksAttacking, "name": "Find all rooks targeting a square"},
            {"runnable": cls.bishopsAttacking, "name": "Find all bishops targeting a square"},
            {"runnable": cls.queensAttacking, "name": "Find all queens targeting a square"},
            {"runnable": cls.knightsAttacking, "name": "Find all knights targeting a square"},
            {"runnable": cls.pawnsAttacking, "name": "Find all pawns targeting a square"},
            {"runnable": cls.pawnsWalkingTo, "name": "Find all pawns walking to a square"},
            {"runnable": cls.dangerousPawnAttacks, "name": "Handle pawns targeting dangerous squares"},
            {"runnable": cls.dangerousPawnWalks, "name": "Handle pawns walking to dangerous squares"},
        ]
    
    @staticmethod
    def initializeEmptyBoard():
        board = Board()
        return True

    @staticmethod
    def boardHasSquares():
        squares = Board()._squares
        assert(squares)
        assert(len(squares) == 8), squares
        assert(all([len(row) == 8 for row in squares])), squares
        assert(all([(square == '-' for square in row) for row in squares])), squares
        return True

    @staticmethod    
    def emptyBoardFromFen():
        emptyBoard = Board.fromFEN("8/8/8/8/8/8/8/8")
        assert(emptyBoard._squares == Board()._squares)
        return True
    
    @staticmethod
    def startingBoardFromFEN():
        startingBoard = Board.fromFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        assert(startingBoard._squares[0] == [s for s in "RNBQKBNR"]), startingBoard._squares[0]
        assert(startingBoard._squares[1] == [s for s in "PPPPPPPP"]), startingBoard._squares[1]
        assert(startingBoard._squares[6] == [s for s in "pppppppp"]), startingBoard._squares[6]
        assert(startingBoard._squares[7] == [s for s in "rnbqkbnr"]), startingBoard._squares[7]
        return True
    
    @staticmethod
    def boardEquality():
        assert(Board() == Board())
        startingPos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        assert(Board.fromFEN(startingPos) == Board.fromFEN(startingPos))
        return True

    @staticmethod
    def canSee():
        starBoard = Board.fromFEN("8/3q3k/1Q1Q1Q2/8/qQ1q1Qq1/8/1Q1Q1Q1K/3q4")
        attacker = Vector.fromAN("d4")

        assert(starBoard.pieceCanSee(attacker, Vector.fromAN("b2")))
        assert(starBoard.pieceCanSee(attacker, Vector.fromAN("d2")))
        assert(starBoard.pieceCanSee(attacker, Vector.fromAN("f2")))
        assert(starBoard.pieceCanSee(attacker, Vector.fromAN("b4")))
        assert(starBoard.pieceCanSee(attacker, Vector.fromAN("f4")))
        assert(starBoard.pieceCanSee(attacker, Vector.fromAN("b6")))
        assert(starBoard.pieceCanSee(attacker, Vector.fromAN("d6")))
        assert(starBoard.pieceCanSee(attacker, Vector.fromAN("f6")))
        
        assert(not starBoard.pieceCanSee(attacker, Vector.fromAN("d1")))
        assert(not starBoard.pieceCanSee(attacker, Vector.fromAN("a4")))
        assert(not starBoard.pieceCanSee(attacker, Vector.fromAN("g4")))
        assert(not starBoard.pieceCanSee(attacker, Vector.fromAN("d7")))
        return True
    
    @staticmethod
    def rooksAttacking():
        board = Board.fromFEN("3R4/8/3P4/8/R2K1R1R/8/8/R2r4")
        target = Vector.fromAN("d4")
        attackers: List[Vector] = board.getRooksAttacking(target)
        
        assert(Vector.fromAN("a4") in attackers), attackers
        assert(Vector.fromAN("d8") in attackers), attackers
        assert(Vector.fromAN("f4") in attackers), attackers
        assert(Vector.fromAN("h4") in attackers), attackers
        assert(Vector.fromAN("d1") in attackers), attackers
        assert(Vector.fromAN("a1") not in attackers), attackers
        assert(len(attackers) == 5), attackers
        return True
    
    @staticmethod
    def bishopsAttacking():
        board = Board.fromFEN("8/B5B1/8/4B3/3k4/4P3/8/b2B2B1")
        target = Vector.fromAN("d4")
        attackers: List[Vector] = board.getBishopsAttacking(target)
        
        assert(Vector.fromAN("a7") in attackers), attackers
        assert(Vector.fromAN("e5") in attackers), attackers
        assert(Vector.fromAN("g7") in attackers), attackers
        assert(Vector.fromAN("g1") in attackers), attackers
        assert(Vector.fromAN("a1") in attackers), attackers
        assert(Vector.fromAN("d1") not in attackers), attackers
        assert(len(attackers) == 5), attackers
        return True
    
    @staticmethod
    def queensAttacking():
        board = Board.fromFEN("8/Q2Q2Q1/8/3QQ3/Q2KP1Q1/4P3/8/q2q2Q1")
        target = Vector.fromAN("d4")
        attackers: List[Vector] = board.getQueensAttacking(target)

        assert(Vector.fromAN("a4") in attackers), attackers
        assert(Vector.fromAN("a7") in attackers), attackers
        assert(Vector.fromAN("d5") in attackers), attackers
        assert(Vector.fromAN("d7") in attackers), attackers
        assert(Vector.fromAN("e5") in attackers), attackers
        assert(Vector.fromAN("g7") in attackers), attackers
        assert(Vector.fromAN("g4") in attackers), attackers
        assert(Vector.fromAN("d1") in attackers), attackers
        assert(Vector.fromAN("a1") in attackers), attackers
        assert(len(attackers) == 10), attackers
        return True
    
    @staticmethod
    def knightsAttacking():
        board = Board.fromFEN("8/8/2n1N3/1N3n1N/3K3N/1n3N1N/2N1n3/8")
        target = Vector.fromAN("d4")
        attackers: List[Vector] = board.getKnightsAttacking(target)

        assert(Vector.fromAN("b5") in attackers), attackers
        assert(Vector.fromAN("c6") in attackers), attackers
        assert(Vector.fromAN("e6") in attackers), attackers
        assert(Vector.fromAN("f5") in attackers), attackers
        assert(Vector.fromAN("f3") in attackers), attackers
        assert(Vector.fromAN("e2") in attackers), attackers
        assert(Vector.fromAN("c2") in attackers), attackers
        assert(Vector.fromAN("b3") in attackers), attackers
        assert(Vector.fromAN("h5") not in attackers), attackers
        assert(Vector.fromAN("h6") not in attackers), attackers
        assert(Vector.fromAN("h7") not in attackers), attackers
        assert(len(attackers) == 8), attackers
        return True 
    
    @staticmethod
    def pawnsAttacking():
        board = Board.fromFEN("8/8/8/1pppPPP1/2K2k2/1PPPppp1/8/8")
        validTarget = Vector.fromAN("c4")
        invalidTarget = Vector.fromAN("f4")
        validAtackers: List[Vector] = board.getPawnsAttacking(validTarget)
        invalidAttackers: List[Vector] = board.getPawnsAttacking(invalidTarget)

        assert(Vector.fromAN("b5") in validAtackers), validAtackers
        assert(Vector.fromAN("c5") not in validAtackers), validAtackers
        assert(Vector.fromAN("d5") in validAtackers), validAtackers
        assert(Vector.fromAN("b3") in validAtackers), validAtackers
        assert(Vector.fromAN("c3") not in validAtackers), validAtackers
        assert(Vector.fromAN("d3") in validAtackers), validAtackers
        assert(len(validAtackers) == 4)

        assert(Vector.fromAN("f5") not in invalidAttackers), invalidAttackers
        assert(Vector.fromAN("e5") not in invalidAttackers), invalidAttackers
        assert(Vector.fromAN("g5") not in invalidAttackers), invalidAttackers
        assert(Vector.fromAN("e3") not in invalidAttackers), invalidAttackers
        assert(Vector.fromAN("f3") not in invalidAttackers), invalidAttackers
        assert(Vector.fromAN("g3") not in invalidAttackers), invalidAttackers
        assert(len(invalidAttackers) == 0), invalidAttackers
        return True

    @staticmethod
    def pawnsWalkingTo():
        board = Board.fromFEN("3k4/3P1pp1/4p1p1/3PKKKK/kkkk3p/P1P5/1PP4p/7K")
        aFile = board.getPawnsWalkingTo(Vector.fromAN("a4"))
        bFile = board.getPawnsWalkingTo(Vector.fromAN("b4"))
        cFile = board.getPawnsWalkingTo(Vector.fromAN("c4"))
        dFile = board.getPawnsWalkingTo(Vector.fromAN("d4"))
        dFile2 = board.getPawnsWalkingTo(Vector.fromAN("d8"))
        eFile = board.getPawnsWalkingTo(Vector.fromAN("e5"))
        fFile = board.getPawnsWalkingTo(Vector.fromAN("f5"))
        gFile = board.getPawnsWalkingTo(Vector.fromAN("g5"))
        hFile = board.getPawnsWalkingTo(Vector.fromAN("h5"))
        hFile2 = board.getPawnsWalkingTo(Vector.fromAN("h1"))

        assert(Vector.fromAN("a3") in aFile and len(aFile) == 1), aFile
        assert(Vector.fromAN("b2") in bFile and len(bFile) == 1), bFile
        assert(Vector.fromAN("b3") not in bFile and len(bFile) == 1), bFile
        assert(Vector.fromAN("c2") in cFile and len(cFile) == 2), cFile
        assert(Vector.fromAN("c3") in cFile and len(cFile) == 2), cFile
        assert(Vector.fromAN("d5") not in dFile and len(dFile) == 0), dFile
        assert(Vector.fromAN("d7") in dFile2 and len(dFile2) == 1), dFile2
        assert(Vector.fromAN("e6") in eFile and len(eFile) == 1), eFile
        assert(Vector.fromAN("f7") in fFile and len(fFile) == 1), fFile
        assert(Vector.fromAN("g6") in gFile and len(gFile) == 2), gFile
        assert(Vector.fromAN("g7") in gFile and len(gFile) == 2), gFile
        assert(Vector.fromAN("h4") not in hFile and len(hFile) == 0), hFile2
        assert(Vector.fromAN("h2") in hFile2 and len(hFile2) == 1), hFile2
        return True
    
    @staticmethod
    def dangerousPawnAttacks():
        whiteCorners = Board.fromFEN("P6P/8/8/8/8/8/8/P6P w - - 0 1")
        whiteCorners.getPawnsAttacking(Vector.fromAN("a1"))
        whiteCorners.getPawnsAttacking(Vector.fromAN("a8"))
        whiteCorners.getPawnsAttacking(Vector.fromAN("h1"))
        whiteCorners.getPawnsAttacking(Vector.fromAN("h8"))
        whiteCorners.getPawnsAttacking(Vector.fromAN("b2"))
        whiteCorners.getPawnsAttacking(Vector.fromAN("b7"))
        whiteCorners.getPawnsAttacking(Vector.fromAN("g2"))
        whiteCorners.getPawnsAttacking(Vector.fromAN("g7"))

        blackCorners = Board.fromFEN("p6p/8/8/8/8/8/8/p6p w - - 0 1")
        blackCorners.getPawnsAttacking(Vector.fromAN("a1"))
        blackCorners.getPawnsAttacking(Vector.fromAN("a8"))
        blackCorners.getPawnsAttacking(Vector.fromAN("h1"))
        blackCorners.getPawnsAttacking(Vector.fromAN("h8"))
        blackCorners.getPawnsAttacking(Vector.fromAN("b2"))
        blackCorners.getPawnsAttacking(Vector.fromAN("b7"))
        blackCorners.getPawnsAttacking(Vector.fromAN("g2"))
        blackCorners.getPawnsAttacking(Vector.fromAN("g7"))
        return True
    
    @staticmethod
    def dangerousPawnWalks():
        whiteCorners = Board.fromFEN("P6P/8/8/8/8/8/8/P6P w - - 0 1")
        whiteCorners.getPawnsWalkingTo(Vector.fromAN("a1"))
        whiteCorners.getPawnsWalkingTo(Vector.fromAN("a8"))
        whiteCorners.getPawnsWalkingTo(Vector.fromAN("h1"))
        whiteCorners.getPawnsWalkingTo(Vector.fromAN("h8"))

        blackCorners = Board.fromFEN("p6p/8/8/8/8/8/8/p6p w - - 0 1")
        blackCorners.getPawnsWalkingTo(Vector.fromAN("a1"))
        blackCorners.getPawnsWalkingTo(Vector.fromAN("a8"))
        blackCorners.getPawnsWalkingTo(Vector.fromAN("h1"))
        blackCorners.getPawnsWalkingTo(Vector.fromAN("h8"))
        return True