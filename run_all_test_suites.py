from vector_test_suite import VectorTestSuite
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
        {"suite_name": "VEC", "test_list": VectorTestSuite.getTests()},
        {"suite_name": "MOV", "test_list": MoveTestSuite.getTests()},
        {"suite_name": "POS", "test_list": PositionTestSuite.getTests()},
        {"suite_name": "GEN", "test_list": MoveGeneratorTestSuite.getTests()},
        {"suite_name": "VER", "test_list": MoveVerifierTestSuite.getTests()}
    ]
    allTestsPassed = True
    testsPassed = 0 
    testsRun = 0
    for suite in test_suites:
        test_number = 0
        print("-- %s ---:----->" % suite["suite_name"])
        for test in suite["test_list"]:
            testsRun += 1
            test_number += 1
            result = False
            try:
                result = test["runnable"]()
                if result == False:
                    allTestsPassed = False
                else:
                    testsPassed += 1
            except Exception as e:
                allTestsPassed = False
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
    print(colorama.Fore.GREEN if allTestsPassed == True else colorama.Fore.RED)
    print("%d out of %d tests passed! %s\n (%d percent success rate)" % (testsPassed, testsRun, colorama.Style.RESET_ALL, (testsPassed * 100 / testsRun)))
    print()
    
if __name__ == "__main__":
    main()

