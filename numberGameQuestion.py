import sys

maxNumberPlayers = 5
keyBackToMenu = "-"

def showMenu():
    print("Welcome to the Game")
    print("Please select and option:")
    print("1. Normal Game")
    print("2. Scoring Modified Game")
    print("3. Game with Trap")
    print("4. Game with Reverse Turn Directions")
    print("5. Exit")

def showNumberPlayersQuestion(maxNumberPlayers, keyBackToMenu):
    print("Indicate the number of players for the game. Minimum", 2, "and Maximum", maxNumberPlayers)
    print("Use the value", keyBackToMenu, "to go back to main menu")

def fakeClearScreen():
    for numberLine in range(50):
        print("")

def askMenuOption():
    optionSelected = 0
    while optionSelected not in range(1, 6):
        fakeClearScreen()
        showMenu()
        print("Option")
        try:
            optionSelected = int(sys.stdin.readline().strip())
        except ValueError:
            optionSelected = 0
    return optionSelected

def askNumberPlayers(maxNumberPlayers, keyBackToMenu):
    numberPlayers = 0
    while numberPlayers not in range(2, maxNumberPlayers + 1):
        fakeClearScreen()
        showNumberPlayersQuestion(maxNumberPlayers, keyBackToMenu)
        print("Value")
        value = sys.stdin.readline().strip()
        if value != keyBackToMenu:
            try:
                numberPlayers = int(value)
            except ValueError:
                numberPlayers = 0
        else:
            numberPlayers = keyBackToMenu
            break
    return numberPlayers

programExit = False
while programExit == False:
    optionSelected = askMenuOption()
    if optionSelected == 1:
        numberPlayers = askNumberPlayers(maxNumberPlayers, keyBackToMenu)
        if numberPlayers != keyBackToMenu:
            print("LETS PLAY")
    elif optionSelected == 2:
        numberPlayers = askNumberPlayers(maxNumberPlayers, keyBackToMenu)
        if numberPlayers != keyBackToMenu:
            print("LETS PLAY")
    elif optionSelected == 3:
        numberPlayers = askNumberPlayers(maxNumberPlayers, keyBackToMenu)
        if numberPlayers != keyBackToMenu:
            print("LETS PLAY")
    elif optionSelected == 4:
        numberPlayers = askNumberPlayers(maxNumberPlayers, keyBackToMenu)
        if numberPlayers != keyBackToMenu:
            print("LETS PLAY")
    elif optionSelected == 5:
        programExit = True