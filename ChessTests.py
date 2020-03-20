from Chess import *

"""
These tests check whether the implementation of
Chess.py correctly follows the FIDE rules of chess.
"""

"""
[Article 1.1] - What is Chess
The game of chess is played between two opponents who move their pieces alternately
on a square board called a ‘chessboard’. The player with the white pieces commences the
game. A player is said to ‘have the move’, when his opponent’s move has been ‘made’.
"""

def test_1_1_a():
    'The game takes place on a chessboard'
    chessboard = Chessboard()
    print("[1.1.a][Pass]")
def test_1_1_b():
    'The player with the white pieces starts the game'
    pass
def test_1_1_c():
    'A player "has the move" when his opponents move has been made'
    pass
    


def main():
    print("===================")
    print("=== Chess Tests ===")
    print("===================")
    print("")

    #Article 1 - The nature and objectives of the game of chess
    #Article 1.1
    test_1_1_a()
    test_1_1_b()  
    test_1_1_c()

    print("")
    print("-----------------------------------------")
    print("Test Run Complete, press any key to exit.")
    print("-----------------------------------------")


if (__name__ == "__main__"):
    main()
