from Chess import *

class ChessTests():
    class TestResult():
        def __init__(self, _expected=None, _actual=None):
            self.value = _expected == _actual
            self.expected = _expected
            self.actual = _actual
        
    def testAll():
        tests = {
            1: ChessTests.test_1
        }

        for name, test in tests.items():
            value = False
            error = ""
            try:
                result = test()
                value = result.value

                if (value == False):
                    error = "Expected %s | Recieved %s" %(result.expected, result.actual)
            except Exception as e:
                result = "Error"
                error = e.args[0]
            print("Test [" + str(name) + "] = " + str(value) + " | " + error)

    def test_1():
        #Return the starting state of the board,
        #in Forsyth-Edwards Notation.
        
        expected_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        actual_board = ""

        #Initialize Chessboard
        chessboard = Chessboard()
        actual_board = chessboard.toString()
        
        return ChessTests.TestResult(
            expected_board,
            actual_board
        )
        
        

def main():
    ChessTests.testAll()
main()
