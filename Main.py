from position import Position


def main():
  #Initialize Chessboard
  chessboard = Position.fromStartingPosition()
  chessboard.boardState.toString()
  
  """
  #Ask for tile selection
  x = int(input("What is the X Vector of the piece you want to select?\n"))
  y = int(input("What is the Y Vector of the piece you want to select?\n"))

  #Ask for destination selection
  newX = int(input("Where would you like to move the piece to (X-Vector)?"))
  newY = int(input("Where would you like to move the piece to (Y-Vector)?"))
  
  chessboard.move(x, y, newX, newY)

  #Print resultant board
  print("Final Board State")
  chessboard.draw()
  """

if (__name__ == "__main__"):
  main()