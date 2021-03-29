import Chess


def main():
  #Initialize Chessboard
  chessboard = Chess.Chessboard()
  print(chessboard.toString())

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