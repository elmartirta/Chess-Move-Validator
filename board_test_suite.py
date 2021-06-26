from board import Board


class BoardTestSuite():
    @classmethod
    def getTests(cls):
        return[
            {"runnable": cls.initializeEmptyBoard, "name": "Initialize a Board object"},
            {"runnable": cls.boardHasSquares, "name": "Board() contains an 8x8 .squares matrix"},
            {"runnable": cls.emptyBoardFromFen, "name": "Initialize a Board object"},
            {"runnable": cls.startingBoardFromFEN, "name": "Initialize a Board object"},
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
    

        
