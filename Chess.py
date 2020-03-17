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

    #Initialize Tiles
    self.tiles = []
    for y in range (0, 8):
      row = []
      for x in range(0, 8):
        row.append(Tile())
      self.tiles.append(row)
    
    def set_to_starter_chessboard(self):
      self.tileAt(0,0).piece = Piece("R", "W")
      self.tileAt(1,0).piece = Piece("N", "W")
      self.tileAt(2,0).piece = Piece("B", "W")
      self.tileAt(3,0).piece = Piece("Q", "W")
      self.tileAt(4,0).piece = Piece("K", "W")
      self.tileAt(5,0).piece = Piece("B", "W")
      self.tileAt(6,0).piece = Piece("N", "W")
      self.tileAt(7,0).piece = Piece("R", "W")
    
      for x in range (0, 8):
        self.tileAt(x, 1).piece = Piece("p", "W")

      self.tileAt(0,7).piece = Piece("R", "B")
      self.tileAt(1,7).piece = Piece("N", "B")
      self.tileAt(2,7).piece = Piece("B", "B")
      self.tileAt(3,7).piece = Piece("Q", "B")
      self.tileAt(4,7).piece = Piece("K", "B")
      self.tileAt(5,7).piece = Piece("B", "B")
      self.tileAt(6,7).piece = Piece("N", "B")
      self.tileAt(7,7).piece = Piece("R", "B")

      for x in range (0, 8):
        self.tileAt(x, 6).piece = Piece("p", "B")
    set_to_starter_chessboard(self)
    
  def tileAt(self, x, y):
    return self.tiles[y][x]

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
  tile = chessboard.tileAt(x,y)
  print("The Piece you selected is (%s)" %(tile.piece))

  #Ask for destination selection
  newX = int(input("Where would you like to move the piece to (X-Coordinate)?"))
  newY = int(input("Where would you like to move the piece to (Y-Coordinate)?"))
  newTile = chessboard.tileAt(newX, newY)
  print("The Tile you will replace is (%s)" % (newTile.piece))

  #Move piece from selection to destination
  selectedPiece = tile.piece
  newTile.piece = selectedPiece
  tile.removePiece()

  #Print resultant board
  print("Final Board State")
  chessboard.draw()

main()
