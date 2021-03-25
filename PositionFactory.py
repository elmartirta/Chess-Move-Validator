import Position
from Position import AlgebraicNotation as AN
class PositionFactory():
    def fromFEN(fen):
        pass;
    def getStartingPosition():
        pos = Position();

        pos.boardState.addPiece(AN("a1"),"r");
        pos.boardState.addPiece(AN("b1"),"n");
        pos.boardState.addPiece(AN("c1"),"b");
        pos.boardState.addPiece(AN("d1"),"q");
        pos.boardState.addPiece(AN("e1"),"k");
        pos.boardState.addPiece(AN("f1"),"b");
        pos.boardState.addPiece(AN("g1"),"n");
        pos.boardState.addPiece(AN("h1"),"r");

        pos.boardState.addPiece(AN("a2"), "p");
        pos.boardState.addPiece(AN("b2"), "p");
        pos.boardState.addPiece(AN("c2"), "p");
        pos.boardState.addPiece(AN("d2"), "p");
        pos.boardState.addPiece(AN("e2"), "p");
        pos.boardState.addPiece(AN("f2"), "p");
        pos.boardState.addPiece(AN("g2"), "p");
        pos.boardState.addPiece(AN("h2"), "p");
        
        pos.boardState.addPiece(AN("a7"), "p");
        pos.boardState.addPiece(AN("b7"), "p");
        pos.boardState.addPiece(AN("c7"), "p");
        pos.boardState.addPiece(AN("d7"), "p");
        pos.boardState.addPiece(AN("e7"), "p");
        pos.boardState.addPiece(AN("f7"), "p");
        pos.boardState.addPiece(AN("g7"), "p");
        pos.boardState.addPiece(AN("h7"), "p");
        
        pos.boardState.addPiece(AN("a8"),"r");
        pos.boardState.addPiece(AN("b8"),"n");
        pos.boardState.addPiece(AN("c8"),"b");
        pos.boardState.addPiece(AN("d8"),"q");
        pos.boardState.addPiece(AN("e8"),"k");
        pos.boardState.addPiece(AN("f8"),"b");
        pos.boardState.addPiece(AN("g8"),"n");
        pos.boardState.addPiece(AN("h8"),"r");

        return pos