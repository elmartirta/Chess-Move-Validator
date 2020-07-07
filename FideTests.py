from Chess import *

"""
These tests check whether the implementation of
Chess.py correctly follows the FIDE rules of chess.
"""

'FIDE Article [3.2] : A bishop may move to any square along a diagonal which it stands'
def test_3_2_a():
    #Initialize black bishop at e4
    #Test moves Be4 -> a8, b7, c6, d5, e4, f3, g2, h1 == Legal
    #Test moves Be4 -> b1, c2, d3, f5, g6, h7 == Legal
    pass
def test_3_2_b():    
    #Initialize white bishop at e4
    #Test moves Be4 -> a8, b7, c6, d5, e4, f3, g2, h1
    #Test moves Be4 -> b1, c2, d3, f5, g6, h7
    #Randomly test 10 moves not part of that set
    pass
def test_3_2_c():
    #Test move White : Ba1 Bh7 == Legal
    #Test move White : Bh7 Ba1 == Legal
    #Test move White : Ba7 Bh1 == Legal
    #Test move White : Bh1 Ba7 == Legal
    pass
def test_3_2_d():
    #Test move Black : Ba1 Bh7 == Legal
    #Test move Black : Bh7 Ba1 == Legal
    #Test move Black : Ba7 Bh1 == Legal
    #Test move Black : Bh1 Ba7 == Legal
    pass
def test_3_2_e():
    #Randomly test 10 moves not part of the set
    #e4 -> [a8, b7, c6, d5, e4, f3, g2, h1, b1, c2, d3, f5, g6, h7]
    #Assert False
    pass

def main():
    print("===================")
    print("=== Chess Tests ===")
    print("===================")
    print("")

    test_3_2_a()
    test_3_2_b()
    test_3_2_c()
    test_3_2_d()
    test_3_2_e()
    
    def draw_test():
        print ("Test M_1: Draw Test")
        print ("")
        board = Chessboard()
        board.draw()
        print ("")
        print("Test M_1: Complete!")
    draw_test()
    
    print("")
    print("-----------------------------------------")
    print("Test Run Complete, press any key to exit.")
    print("-----------------------------------------")


if (__name__ == "__main__"):
    main()
