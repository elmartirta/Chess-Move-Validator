import Position
from Position import CartesianCoordinate as Coord
class PositionFactory():
    def fromFEN(fen):
        pass
    def fromStartingPosition():
        position = Position()
        board = board
        startingConfiguration = [
            ("a1","r"),
            ("b1","n"),
            ("c1","b"),
            ("d1","q"),
            ("e1","k"),
            ("f1","b"),
            ("g1","n"),
            ("h1","r"),

            ("a2", "p"),
            ("b2", "p"),
            ("c2", "p"),
            ("d2", "p"),
            ("e2", "p"),
            ("f2", "p"),
            ("g2", "p"),
            ("h2", "p"),
            
            ("a7", "p"),
            ("b7", "p"),
            ("c7", "p"),
            ("d7", "p"),
            ("e7", "p"),
            ("f7", "p"),
            ("g7", "p"),
            ("h7", "p"),
            
            ("a8","r"),
            ("b8","n"),
            ("c8","b"),
            ("d8","q"),
            ("e8","k"),
            ("f8","b"),
            ("g8","n"),
            ("h8","r")
        ]
        for (pieceLocation in startingConfiguration){
            pieceType = pieceLocation[0];
            location = pieceLocation[1];
            board.addPiece.(Coord.fromAN(location), pieceType)
        }
        return position