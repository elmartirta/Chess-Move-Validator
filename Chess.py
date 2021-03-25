class Chessboard():
  '''This class represents a chessboard'''
  def __init__(self):
    '''Create a chessboard'''
    self.tiles = [[Tile() for x in range(8)] for y in range(8)]
    
    def set_to_starter_chessboard(self):
      self.tileAt(0,0).piece = Piece("r", "W")
      self.tileAt(1,0).piece = Piece("n", "W")
      self.tileAt(2,0).piece = Piece("b", "W")
      self.tileAt(3,0).piece = Piece("q", "W")
      self.tileAt(4,0).piece = Piece("k", "W")
      self.tileAt(5,0).piece = Piece("b", "W")
      self.tileAt(6,0).piece = Piece("n", "W")
      self.tileAt(7,0).piece = Piece("r", "W")
    
      for tile in self.rowAt(1):
        tile.piece = Piece("p", "W")
        
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

    move = (x2-x1, y2-y1)
    legal_moves = sourceTile.piece.legalMoves()
    if not(move in legal_moves):
      return {"result": False, "reason": "The piece must follow its own rules"}
    
    for path_tile in legal_moves[move]["Path"]:
      path_coord = tuple(sum(x) for x in zip((x1,y1), path_tile))
      if (self.tileAt(*path_coord).hasPiece()): 
        return {"result": False, "reason": "There cannot be a piece in the path of the moving piece."}

    if (self.isKingInCheck(sourceTile.piece.faction)):
      return {"result": False, "reason": "The King cannot be in check."}
    
    #The final board state can not end with the allied king in check.

    return {"result":True} #stub
  
  def isKingInCheck(self, faction):
    return False #stub
    
  def toString(self):
    output = ""
    for row in self.tiles:
      rowString = ""
      for piece in row:
        rowString += str(piece)
      output += rowString + "\n"
    return output

  def toFEN_placement(self):
    output = ""
    for row in self.tiles:
      spaceCount=0
      rowString = ""
      for piece in row:
        if str(piece) == "-":
          spaceCount += 1
        else:
          rowString += str(piece)
      if spaceCount != 0:
        output += str(spaceCount)
      output += rowString + "/"
    return output[:-1]


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
    self.faction = faction
  def __str__(self):
    if (self.faction == "W"):
      return self.label
    else:
      return self.label.upper()

  def legalMoves(self):    
    if self.label == "p" and self.faction == "W":
      return {
        (0,1):{"Path":[]}
      }
    if self.label == "p" and self.faction == "B":
      return {
        (0,-1):{"Path":[]}
      }
    if self.label == "r":
      return {
        ( 0, 1):{"Path": []},
        ( 0, 2):{"Path": [(0,1)]},
        ( 0, 3):{"Path": [(0,1),(0,2)]},
        ( 0, 4):{"Path": [(0,1),(0,2),(0,3)]},
        ( 0, 5):{"Path": [(0,1),(0,2),(0,3),(0,4)]},
        ( 0, 6):{"Path": [(0,1),(0,2),(0,3),(0,4),(0,5)]},
        ( 0, 7):{"Path": [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6)]},
        ( 0,-1):{"Path": []},
        ( 0,-2):{"Path": [(0,-1)]},
        ( 0,-3):{"Path": [(0,-1),(0,-2)]},
        ( 0,-4):{"Path": [(0,-1),(0,-2),(0,-3)]},
        ( 0,-5):{"Path": [(0,-1),(0,-2),(0,-3),(0,-4)]},
        ( 0,-6):{"Path": [(0,-1),(0,-2),(0,-3),(0,-4),(0,-5)]},
        ( 0,-7):{"Path": [(0,-1),(0,-2),(0,-3),(0,-4),(0,-5),(0,-6)]},
        ( 1, 0):{"Path": []},
        ( 2, 0):{"Path": [(1,0)]},
        ( 3, 0):{"Path": [(1,0),(2,0)]},
        ( 4, 0):{"Path": [(1,0),(2,0),(3,0)]},
        ( 5, 0):{"Path": [(1,0),(2,0),(3,0),(4,0)]},
        ( 6, 0):{"Path": [(1,0),(2,0),(3,0),(4,0),(5,0)]},
        ( 7, 0):{"Path": [(1,0),(2,0),(3,0),(4,0),(5,0),(6,0)]},
        (-1, 0):{"Path": []},
        (-2, 0):{"Path": [(-1,0)]},
        (-3, 0):{"Path": [(-1,0),(-2,0)]},
        (-4, 0):{"Path": [(-1,0),(-2,0),(-3,0)]},
        (-5, 0):{"Path": [(-1,0),(-2,0),(-3,0),(-4,0)]},
        (-6, 0):{"Path": [(-1,0),(-2,0),(-3,0),(-4,0),(-5,0)]},
        (-7, 0):{"Path": [(-1,0),(-2,0),(-3,0),(-4,0),(-5,0),(-6,0)]}
      }
    if self.label == "n":
      return {
        ( 1, 2):{"Path":[]},
        ( 1,-2):{"Path":[]},
        (-1, 2):{"Path":[]},
        (-1,-2):{"Path":[]},
        ( 2, 1):{"Path":[]},
        ( 2,-1):{"Path":[]},
        (-2, 1):{"Path":[]},
        (-2,-1):{"Path":[]}
      }
    if self.label == "b":
      return {
        ( 1, 1):{"Path":[]},
        ( 2, 2):{"Path":[(1,1)]},
        ( 3, 3):{"Path":[(1,1),(2,2)]},
        ( 4, 4):{"Path":[(1,1),(2,2),(3,3)]},
        ( 5, 5):{"Path":[(1,1),(2,2),(3,3),(4,4)]},
        ( 6, 6):{"Path":[(1,1),(2,2),(3,3),(4,4),(5,5)]},
        ( 7, 7):{"Path":[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6)]},
        (-1, 1):{"Path":[]},
        (-2, 2):{"Path":[(-1,1)]},
        (-3, 3):{"Path":[(-1,1),(-2,2)]},
        (-4, 4):{"Path":[(-1,1),(-2,2),(-3,3)]},
        (-5, 5):{"Path":[(-1,1),(-2,2),(-3,3),(-4,4)]},
        (-6, 6):{"Path":[(-1,1),(-2,2),(-3,3),(-4,4),(-5,5)]},
        (-7, 7):{"Path":[(-1,1),(-2,2),(-3,3),(-4,4),(-5,5),(-6,6)]},
        ( 1,-1):{"Path":[]},
        ( 2,-2):{"Path":[(1,-1)]},
        ( 3,-3):{"Path":[(1,-1),(2,-2)]},
        ( 4,-4):{"Path":[(1,-1),(2,-2),(3,-3)]},
        ( 5,-5):{"Path":[(1,-1),(2,-2),(3,-3),(4,-4)]},
        ( 6,-6):{"Path":[(1,-1),(2,-2),(3,-3),(4,-4),(5,-5)]},
        ( 7,-7):{"Path":[(1,-1),(2,-2),(3,-3),(4,-4),(5,-5),(6,-6)]},
        (-1,-1):{"Path":[]},
        (-2,-2):{"Path":[(-1,-1)]},
        (-3,-3):{"Path":[(-1,-1),(-2,-2)]},
        (-4,-4):{"Path":[(-1,-1),(-2,-2),(-3,-3)]},
        (-5,-5):{"Path":[(-1,-1),(-2,-2),(-3,-3),(-4,-4)]},
        (-6,-6):{"Path":[(-1,-1),(-2,-2),(-3,-3),(-4,-4),(-5,-5)]},
        (-7,-7):{"Path":[(-1,-1),(-2,-2),(-3,-3),(-4,-4),(-5,-5),(-6,-6)]}
      }

    if self.label == "k":
      return {
        ( 1 ,0):{"Path":[]},
        (-1, 0):{"Path":[]},
        ( 0, 1):{"Path":[]},
        ( 0,-1):{"Path":[]},
        ( 1, 1):{"Path":[]},
        ( 1,-1):{"Path":[]},
        (-1, 1):{"Path":[]},
        (-1,-1):{"Path":[]}
      }
    if self.label == "q":
      return {
        ( 0, 1):{"Path": []},
        ( 0, 2):{"Path": [(0,1)]},
        ( 0, 3):{"Path": [(0,1),(0,2)]},
        ( 0, 4):{"Path": [(0,1),(0,2),(0,3)]},
        ( 0, 5):{"Path": [(0,1),(0,2),(0,3),(0,4)]},
        ( 0, 6):{"Path": [(0,1),(0,2),(0,3),(0,4),(0,5)]},
        ( 0, 7):{"Path": [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6)]},
        ( 0,-1):{"Path": []},
        ( 0,-2):{"Path": [(0,-1)]},
        ( 0,-3):{"Path": [(0,-1),(0,-2)]},
        ( 0,-4):{"Path": [(0,-1),(0,-2),(0,-3)]},
        ( 0,-5):{"Path": [(0,-1),(0,-2),(0,-3),(0,-4)]},
        ( 0,-6):{"Path": [(0,-1),(0,-2),(0,-3),(0,-4),(0,-5)]},
        ( 0,-7):{"Path": [(0,-1),(0,-2),(0,-3),(0,-4),(0,-5),(0,-6)]},
        ( 1, 0):{"Path": []},
        ( 2, 0):{"Path": [(1,0)]},
        ( 3, 0):{"Path": [(1,0),(2,0)]},
        ( 4, 0):{"Path": [(1,0),(2,0),(3,0)]},
        ( 5, 0):{"Path": [(1,0),(2,0),(3,0),(4,0)]},
        ( 6, 0):{"Path": [(1,0),(2,0),(3,0),(4,0),(5,0)]},
        ( 7, 0):{"Path": [(1,0),(2,0),(3,0),(4,0),(5,0),(6,0)]},
        (-1, 0):{"Path": []},
        (-2, 0):{"Path": [(-1,0)]},
        (-3, 0):{"Path": [(-1,0),(-2,0)]},
        (-4, 0):{"Path": [(-1,0),(-2,0),(-3,0)]},
        (-5, 0):{"Path": [(-1,0),(-2,0),(-3,0),(-4,0)]},
        (-6, 0):{"Path": [(-1,0),(-2,0),(-3,0),(-4,0),(-5,0)]},
        (-7, 0):{"Path": [(-1,0),(-2,0),(-3,0),(-4,0),(-5,0),(-6,0)]},        
        ( 1, 1):{"Path":[]},
        ( 2, 2):{"Path":[(1,1)]},
        ( 3, 3):{"Path":[(1,1),(2,2)]},
        ( 4, 4):{"Path":[(1,1),(2,2),(3,3)]},
        ( 5, 5):{"Path":[(1,1),(2,2),(3,3),(4,4)]},
        ( 6, 6):{"Path":[(1,1),(2,2),(3,3),(4,4),(5,5)]},
        ( 7, 7):{"Path":[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6)]},
        (-1, 1):{"Path":[]},
        (-2, 2):{"Path":[(-1,1)]},
        (-3, 3):{"Path":[(-1,1),(-2,2)]},
        (-4, 4):{"Path":[(-1,1),(-2,2),(-3,3)]},
        (-5, 5):{"Path":[(-1,1),(-2,2),(-3,3),(-4,4)]},
        (-6, 6):{"Path":[(-1,1),(-2,2),(-3,3),(-4,4),(-5,5)]},
        (-7, 7):{"Path":[(-1,1),(-2,2),(-3,3),(-4,4),(-5,5),(-6,6)]},
        ( 1,-1):{"Path":[]},
        ( 2,-2):{"Path":[(1,-1)]},
        ( 3,-3):{"Path":[(1,-1),(2,-2)]},
        ( 4,-4):{"Path":[(1,-1),(2,-2),(3,-3)]},
        ( 5,-5):{"Path":[(1,-1),(2,-2),(3,-3),(4,-4)]},
        ( 6,-6):{"Path":[(1,-1),(2,-2),(3,-3),(4,-4),(5,-5)]},
        ( 7,-7):{"Path":[(1,-1),(2,-2),(3,-3),(4,-4),(5,-5),(6,-6)]},
        (-1,-1):{"Path":[]},
        (-2,-2):{"Path":[(-1,-1)]},
        (-3,-3):{"Path":[(-1,-1),(-2,-2)]},
        (-4,-4):{"Path":[(-1,-1),(-2,-2),(-3,-3)]},
        (-5,-5):{"Path":[(-1,-1),(-2,-2),(-3,-3),(-4,-4)]},
        (-6,-6):{"Path":[(-1,-1),(-2,-2),(-3,-3),(-4,-4),(-5,-5)]},
        (-7,-7):{"Path":[(-1,-1),(-2,-2),(-3,-3),(-4,-4),(-5,-5),(-6,-6)]}
      }
    return {}


    



def main():
  #Initialize Chessboard
  chessboard = Chessboard();
  print(chessboard.toString());

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

if (__name__ == "__main__"):
  main()
