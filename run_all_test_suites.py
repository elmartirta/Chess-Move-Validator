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
    summaryString = ""
    for suite in test_suites:
        test_number = 0
        print("-- %s ---:----->" % suite["suite_name"])
        summaryString += suite["suite_name"][0]
        for test in suite["test_list"]:
            testsRun += 1
            test_number += 1
            result = None
            try:
                result = test["runnable"]()
                if result == False:
                    allTestsPassed = False
                    summaryString += (colorama.Fore.RED+"-"+colorama.Style.RESET_ALL)
                else:
                    testsPassed += 1
                    if result is None:
                        summaryString += (colorama.Fore.CYAN+"u"+colorama.Style.RESET_ALL)
                    else:
                        summaryString += (colorama.Fore.GREEN+"+"+colorama.Style.RESET_ALL)
            except Exception as e:
                allTestsPassed = False
                print("["+colorama.Fore.YELLOW+"EXPT"+colorama.Style.RESET_ALL+"] %2d : !!!!!! Exception !!!!!!" % ( test_number))
                print(colorama.Fore.YELLOW)
                traceback.print_exc()
                print(colorama.Style.RESET_ALL)
                summaryString += colorama.Fore.YELLOW+"x"+colorama.Style.RESET_ALL

            finally:
                print("[%s] %2d : %s" % (
                    colorama.Fore.GREEN+"PASS"+colorama.Style.RESET_ALL if result == True else colorama.Fore.RED+"FAIL"+colorama.Style.RESET_ALL if result == False else colorama.Fore.CYAN+"UNDF"+colorama.Style.RESET_ALL, 
                    test_number, 
                    test["name"])
                )
    print(colorama.Fore.GREEN if allTestsPassed == True else colorama.Fore.RED)
    print("%d out of %d tests passed! %s\n (%d percent success rate)" % (testsPassed, testsRun, colorama.Style.RESET_ALL, (testsPassed * 100 / testsRun)))
    print("[%s]" % summaryString)
    print()
    
if __name__ == "__main__":
    main()

