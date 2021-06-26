from notation_parser_test_suite import NotationParserTestSuite
from board_test_suite import BoardTestSuite
from vector_test_suite import VectorTestSuite
from move_test_suite import MoveTestSuite
from position_test_suite import PositionTestSuite
from move_generator_test_suite import MoveGeneratorTestSuite
from move_verifier_test_suite import MoveVerifierTestSuite
from colorama import Fore, Style # type: ignore
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
        {"suite_name": "BOD", "test_list": BoardTestSuite.getTests()},
        {"suite_name": "POS", "test_list": PositionTestSuite.getTests()},
        {"suite_name": "NTN", "test_list": NotationParserTestSuite.getTests()},
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
                    summaryString += Fore.RED + "-" + Style.RESET_ALL
                else:
                    testsPassed += 1
                    if result == True:
                        summaryString += Fore.GREEN + "+" + Style.RESET_ALL
                    else:
                        summaryString += Fore.CYAN + "u" + Style.RESET_ALL
            except Exception as e:
                allTestsPassed = False
                summaryString += Fore.YELLOW+"x"+Style.RESET_ALL
                print(Fore.YELLOW + "=== !!!!!! Exception !!!!!! ===")
                traceback.print_exc()
                print(Style.RESET_ALL)
                result = Exception
                

            finally:
                if result == True:
                    resText = Fore.GREEN + "PASS"
                elif result == False:
                    resText = Fore.RED + "FAIL"
                elif result == Exception:
                    resText = Fore.YELLOW + "EXPT"
                else:
                    resText = Fore.CYAN + "UNDF" 
                print("[%s] %2d : %s" % (
                    resText + Style.RESET_ALL,
                    test_number, 
                    test["name"])
                )
    print(
        "\n%s%d out of %d tests passed! %s\n (%d percent success rate)\n" 
        % (
            Fore.GREEN if allTestsPassed == True else Fore.RED,
            testsPassed, 
            testsRun, 
            Style.RESET_ALL, 
            (testsPassed * 100 / testsRun)
        ))
    print("[%s]" % summaryString)
    if allTestsPassed:
        print("\nAll Tests Passed!!!\n")
    else:
        print("\n===TEST FAILURE===\n")
    
    
if __name__ == "__main__":
    main()

