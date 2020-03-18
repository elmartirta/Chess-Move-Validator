'''
SUCCESS CRITERIA

1. [complete] DRAW A FULL CHESSBOARD TO THE SCREEN
2. ALLOW PLAYERS TO MANUALLY MOVE PIECES (WITHOUT RULES)
3. ADD THE RULES OF CHESS TO THE GAME
4. SHOW WHAT SPACES ARE POSSIBLE TO THE PLAYERS

---Architecture required for Goal 2---
[COMPLETE] Every tile is selectable
Every piece has a faction (black or white)
If a tile has a piece on it, and is clicked, that piece is selected
If a tile is empty, and the player has selected a piece, the selected piece is moved to the new tile
If a tile has an enemy, and the player has selected a piece, the enemy piece is destroyed, and the player's piece is moved.

--- Architecture required for Goal 3 ---
Every piece has a type.
Each piece can move in different ways.
Each piece can attack in different ways.

Each player has a King.
If the player's King is dead, the game is over.
A player must be able to resign.
--ADVANCED--If the player's King is threatened, a check becomes active.
--ADVANCED--If a player's King has nowhere to move, that is checkmate.

--- Architecture required for Goal 4 ---
If a piece is selected, then suggested moves are printed to a layer above the board.
All legal moves must be involved
--ADVANCED-- if the player's King is in check, then the only moves shown must get the king out of check.
'''

#Every tile has a notation (a1, b3, c4)


class Chessboard():
  '''This class represents a chessboard'''
  def __init__(self):
    '''Create a chessboard'''
    self.tiles = [[Tile() for x in range(8)] for y in range(8)]
    
    def set_to_starter_chessboard(self):
      self.tileAt(0,0).piece = Piece("R", "W")
      self.tileAt(1,0).piece = Piece("N", "W")
      self.tileAt(2,0).piece = Piece("B", "W")
      self.tileAt(3,0).piece = Piece("Q", "W")
      self.tileAt(4,0).piece = Piece("K", "W")
      self.tileAt(5,0).piece = Piece("B", "W")
      self.tileAt(6,0).piece = Piece("N", "W")
      self.tileAt(7,0).piece = Piece("R", "W")
    
      for tile in self.rowAt(1):
        tile.piece = Piece("P", "W")
        
      for tile in self.rowAt(6):
        tile.piece = Piece("p", "B")
        
      self.tileAt(0,7).piece = Piece("r", "B")
      self.tileAt(1,7).piece = Piece("n", "B")
      self.tileAt(2,7).piece = Piece("b", "B")
      self.tileAt(3,7).piece = Piece("q", "B")
      self.tileAt(4,7).piece = Piece("k", "B")
      self.tileAt(5,7).piece = Piece("b", "B")
      self.tileAt(6,7).piece = Piece("n", "B")
      self.tileAt(7,7).piece = Piece("r", "B")   
    set_to_starter_chessboard(self)

  def tileAt(self, x, y):
    return self.tiles[y][x]

  def rowAt(self, y):
    return self.tiles[y]

  def swap(self, x1,y1, x2,y2):
    tile_1 = self.tileAt(x1,y1)
    tile_2 = self.tileAt(x2,y2)
    tile_1.piece, tile_2.piece = tile_2.piece, tile_1.piece

  def clear(self, x, y):
    self.tileAt(x,y).piece = None

  def move(self, x1,y1,x2,y2):
    moveIsLegal = self.isMoveLegal(x1,y1,x2,y2)
    if moveIsLegal["result"]:
      self.clear(x2,y2)
      self.swap(x1,y1,x2,y2)
      return {"result":True}
    else:
      print("Error: "+moveIsLegal["reason"])
      return {"result":False}

  def isMoveLegal(self,x1,y1,x2,y2):
    """Returns whether or not moving a piece
    from (x1,y1) to (x2,y2) is a legal move"""
    if(x1 < 0 or x1 > 8 or y1 < 0 or y1 > 8): return {"result":False, "reason": "The piece must exist on the board"}
    if(x1 < 0 or x2 > 8 or y2 < 0 or y2 > 8): return {"result":False, "reason": "The destination location must exist on the board"}
    if(x1 == x2 and y1 == y2): return {"result":False, "reason": "The piece must move to a different location than it started from"}

    sourceTile = self.tileAt(x1,y1)
    destTile = self.tileAt(x2,y2)

    if(not sourceTile.hasPiece()): return {"result": False, "reason": "There must be a piece within the source tile."}
    if(destTile.hasPiece() and sourceTile.piece.faction == destTile.piece.faction):
      return {"result": False, "reason": "The piece may not move into the same square as an allied piece."}

    #A Piece must move according to the piece's rules

    #Spaces that need to be free for the move to be, must be free

    #The final board state can not end with the king in check.

    return {"result":True} #stub
  def draw(self):
    for row in self.tiles:
      rowString = ""
      for piece in row:
        rowString += str(piece)
      print(rowString)


class Tile():
  '''This class represents a tile on a chessboard'''
  def __init__(self):
    self.piece = None

  def __repr__(self):
    if self.piece == None: return "-"
    else: return str(self.piece)
    
  def __str__(self):
    return self.__repr__()

  def removePiece(self):
    #Removes the piece from the tile
    self.piece = None

  def hasPiece(self):
    return (self.piece != None)

class Piece():
  def __init__(self, label=None, faction=None):
    self.label = label
    self.faction = None
  def __str__(self):
    return self.label or "?"




def main():
  #Initialize Chessboard
  chessboard = Chessboard();
  chessboard.draw();

  #Ask for tile selection
  x = int(input("What is the X Coordinate of the piece you want to select?\n"))
  y = int(input("What is the Y Coordinate of the piece you want to select?\n"))

  #Ask for destination selection
  newX = int(input("Where would you like to move the piece to (X-Coordinate)?"))
  newY = int(input("Where would you like to move the piece to (Y-Coordinate)?"))
  
  chessboard.move(x, y, newX, newY)

  #Print resultant board
  print("Final Board State")
  chessboard.draw()

main()
