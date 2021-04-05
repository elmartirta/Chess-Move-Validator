from position_test_suite import PositionTestSuite
from move_verifier_test_suite import MoveVerifierTestSuite
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
        {"suite_name": "VER", "test_list": MoveVerifierTestSuite.getTests()}
    ]
    for suite in test_suites:
        test_number = 0
        for test in suite["test_list"]:
            test_number += 1
            result = False
            try:
                result = test["runnable"]()
            except Exception as e:
                print("[EXPT] %s %2d : !!!!!! Exception !!!!!!" % (suite["suite_name"], test_number))
                traceback.print_exc()
            finally:
                print("[%s] %s %2d : %s" % (
                    "PASS" if result == True else "FAIL" if result == False else "UNDF",
                    suite["suite_name"], 
                    test_number, 
                    test["name"])
                )

    
if __name__ == "__main__":
    main()

