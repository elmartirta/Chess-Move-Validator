from vector2D_test_suite import Vector2DTestSuite
from move_test_suite import MoveTestSuite
from position_test_suite import PositionTestSuite
from move_generator_test_suite import MoveGeneratorTestSuite
from move_verifier_test_suite import MoveVerifierTestSuite
import colorama
import traceback


def main():
    print("")
    print("=== Running Tests ... ===")
    runTests()
    print("=== Tests Complete !!! ===")
    print("")
def runTests():
    test_suites = [
        {"suite_name": "VEC", "test_list": Vector2DTestSuite.getTests()},
        {"suite_name": "MOV", "test_list": MoveTestSuite.getTests()},
        {"suite_name": "POS", "test_list": PositionTestSuite.getTests()},
        {"suite_name": "GEN", "test_list": MoveGeneratorTestSuite.getTests()},
        {"suite_name": "VER", "test_list": MoveVerifierTestSuite.getTests()}
    ]
    for suite in test_suites:
        test_number = 0
        print("-- %s ---:----->" % suite["suite_name"])
        for test in suite["test_list"]:
            test_number += 1
            result = False
            try:
                result = test["runnable"]()
            except Exception as e:
                print("["+colorama.Fore.YELLOW+"EXPT"+colorama.Style.RESET_ALL+"] %2d : !!!!!! Exception !!!!!!" % ( test_number))
                print(colorama.Fore.YELLOW)
                traceback.print_exc()
                print(colorama.Style.RESET_ALL)
            finally:
                print("[%s] %2d : %s" % (
                    colorama.Fore.GREEN+"PASS"+colorama.Style.RESET_ALL if result == True else colorama.Fore.RED+"FAIL"+colorama.Style.RESET_ALL if result == False else colorama.Fore.CYAN+"UNDF"+colorama.Style.RESET_ALL, 
                    test_number, 
                    test["name"])
                )

    
if __name__ == "__main__":
    main()

