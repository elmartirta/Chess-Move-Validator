import pygame
import time



class Piece():
    def __init__(self, name, notation):
        self.name = str(name)
        self.notation = str(notation)
        
class Tile():
    def __init__ (self, x, y, length, piece=None, background=None):
        background = Color.TileColor(x, y) or background
        
        self.x = int(x)
        self.y = int(y)
        self.length = int(length)
        self.piece = piece
        self.background = background
    def rect(self, displayx, displayy):
        return pygame.Rect(
            displayx + self.x * self.length,
            displayy + self.y * self.length,
            self.length,
            self.length)

    def draw(self, surface, x, y):
        #Draws the tile on a surface, with offset X, Y
        color = (self.boardX * 30, self.boardY, self.boardX * 10)
        text = self.font.render(
            self.data[self.boardX][self.boardY],
            False, 
            color)

        displayx = xMargin + x * squareSize
        displayy = yMargin + y * squareSize
        
        screen.blit(text, (x, y))
    
        

    
class Board():
    '''Represents a grid of squares'''
    def __init__(self, width=8, height=8):
        self.width = width;
        self.height = height;
        self.data = [["" for y in range(width)] for x in range(height)]
        self.font = pygame.font.SysFont("comicsansms", 30)
        
    
    def draw(self, surface, x, y, squareSize):
        '''Draws the board on a surface

        Paramaters:
            surface - Pygame Surface Object
            x - x offset in pixels
            y - y offset in pixels
            squareSize - size of the squares in pixels
        '''
        
        for boardY in range(0,self.height):
            for boardX in range(0,self.width):
                self.drawTile(
                    surface,
                    x + boardX * squareSize,
                    y + boardY * squareSize)
                
    def drawTile(self, surface, x, y):
        '''Draws a tile on a surface

        Paramaters:
            surface - Pygame Surface Object
            x - x offset in pixels
            y - y offset in pixels
        '''
        self.drawSquare(screen, xMargin, yMargin, squareSize, x, y)
        self.drawPiece( screen, xMargin, yMargin, squareSize, x, y)
        
    def drawPiece(self, screen, xMargin, yMargin, squareSize, x, y):


    def drawSquare(self, screen, xMargin, yMargin, squareSize, x, y):
            if (x + y) % 2 == 0:
                color = Color.light;
            else:
                color = Color.dark;

            displayx = xMargin + x * squareSize
            displayy = yMargin + y * squareSize
            rect = pygame.Rect(
                displayx,
                displayy,
                squareSize,
                squareSize);
            
            pygame.draw.rect(screen, color, rect)
            Metrics.draw += 1;

                                    
            
class ChessBoard(Board):
    def __init__(self):
        super().__init__(8,8) #m8
        majorpieces = [
            ("WR", "a1"),
            ("WN", "b1"),
            ("WB", "c1"),
            ("WQ", "d1"),
            ("WK", "e1"),
            ("WB", "f1"),
            ("WN", "g1"),
            ("WR", "h1"),
            ("BR", "a8"),
            ("BN", "b8"),
            ("BB", "c8"),
            ("BQ", "d8"),
            ("BK", "e8"),
            ("BB", "f8"),
            ("BN", "g8"),
            ("BR", "h8"),
        ]
        for piece in majorpieces:
            name, loc = piece
            self.insert(name,loc)

        #Places white pawns on row 2
        for i in range (0, 8):
            loc = chr(ord('a') + i) + "2"
            self.insert("WP",  loc);

        #Places black pawns on row 7
        for i in range (0, 8):
            loc = chr(ord('a') + i) + "7"
            self.insert("BP",  loc);
            
    def labelSquares(self):
        for y in range(0, self.height):
            for x in range(0 , self.width):
                row = str(chr(x + ord('a')))
                col = str(self.height-y)
                
                text = row + col
                self.insert(text, text);
                
    def insert(self,string, pos):
        x = ord(pos[0]) - ord('a');
        y = self.height - int(pos[1]);
        self.data[x][y] = str(string);

        
        
class Color():
    light = (255, 206, 158)
    dark = (209, 139, 71)
    def TileColor(x, y):
        if (x + y) % 2 == 0:
            self.background = Color.light;
        else:
            self.background = Color.dark;
