import sys

def main():
    commandLineArgs = sys.argv[1:]
    if len(commandLineArgs) == 0:
        displayTitle()
    else:
        tags = [arg for arg in commandLineArgs if arg.startswith("--")]
        meat = [arg for arg in commandLineArgs if not arg.startswith("--")]
        raise NotImplementedError()


def displayTitle():
    print("------------------------------------")
    print("Welcome to the Chess Move Validator!")
    print("Written by Elmar T.")
    print("------------------------------------")
    displaySelectionMenu()


def displaySelectionMenu():
    while (True):
        print("")
        print("Select an option:")
        print("  [1] Validate a file containing a list of chess moves")
        print("  [2] Manually notate a game of chess")
        print("  [Q] Quit")
        print(">", end="")
        selection = input()

        if not selection:
            print("Please select an option.")
            continue
        elif selection == "1":
            displayFileValidationMenu()
        elif selection == "2":
            displayManualNotation()
        elif selection == "q" or selection == "Q":
            break


def displayFileValidationMenu():
    raise NotImplementedError("File Validation not implemented.")
    

def displayManualNotation():
    raise NotImplementedError("Manual Notation not implemented.")


if (__name__ == "__main__"):
    main()