from position_test_suite import PositionTestSuite
from move_generator_test_suite import MoveGeneratorTestSuite
import traceback


def main():
    print("")
    print("=== Running Tests ... ===")
    runTests()
    print("=== Tests Complete !!! ===")
    print("")
def runTests():
    test_suites = [
        {"suite_name": "POS", "test_list": PositionTestSuite.getTests()},
        {"suite_name": "VER", "test_list": MoveGeneratorTestSuite.getTests()}
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
                print("[EXPT] %2d : !!!!!! Exception !!!!!!" % ( test_number))
                traceback.print_exc()
            finally:
                print("[%s] %2d : %s" % (
                    "PASS" if result == True else "FAIL" if result == False else "UNDF", 
                    test_number, 
                    test["name"])
                )

    
if __name__ == "__main__":
    main()

