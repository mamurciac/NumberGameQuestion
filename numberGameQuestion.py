import sys

maxNumberPlayers = 5
keyBackToMenu = "-"
keyToExit = "+"

normalGameInitialScore = 10

def showMenu():
    print("Welcome to the Game")
    print("Please select and option:")
    print("1. Normal Game")
    print("2. Scoring Modified Game")
    print("3. Game with Trap")
    print("4. Game with Reverse Turn Directions")
    print("5. Exit")

def showNumberPlayersQuestion(maxNumberPlayers, keyBackToMenu, keyToExit):
    print("Indicate the number of players for the game. Minimum", 2, "and Maximum", maxNumberPlayers)
    print("Use the value", keyBackToMenu, "to go back to main menu")
    print("Use the value", keyToExit, "to quit the game")

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

def askNumberPlayers(maxNumberPlayers, keyBackToMenu, keyToExit):
    numberPlayers = 0
    while numberPlayers not in range(2, maxNumberPlayers + 1):
        fakeClearScreen()
        showNumberPlayersQuestion(maxNumberPlayers, keyBackToMenu, keyToExit)
        print("Value")
        value = sys.stdin.readline().strip()
        if value != keyBackToMenu and value != keyToExit:
            try:
                numberPlayers = int(value)
            except ValueError:
                numberPlayers = 0
        else:
            numberPlayers = value
            break
    return numberPlayers

def askNamePlayers(numberPlayers, normalGameInitialScore, keyBackToMenu, keyToExit):
    playerNames = []
    playerScores = {}
    playersAliveInGame = []
    for index in range(numberPlayers):
        fakeClearScreen()
        print("Indicate the name for the player", index + 1)
        print("Use the value", keyBackToMenu, "to go back to main menu")
        print("Use the value", keyToExit, "to quit the game")
        print("Value")
        currentPlayerName = sys.stdin.readline().strip()
        if currentPlayerName == keyBackToMenu:
            playerNames = []
            playerScores = {}
            playersAliveInGame = []
            break
        elif currentPlayerName == keyToExit:
            playerNames = False
            playerScores = False
            playersAliveInGame = False
            break
        else:
            currentPlayerId = str(index + 1) + " - " + currentPlayerName
            playerNames.append(currentPlayerId)
            playerScores[currentPlayerId] = normalGameInitialScore
            playersAliveInGame.append(True)
    return playerNames, playerScores, playersAliveInGame

programExit = False
while programExit == False:
    optionSelected = askMenuOption()
    if optionSelected == 1:
        numberPlayers = askNumberPlayers(maxNumberPlayers, keyBackToMenu, keyToExit)
        if numberPlayers != keyBackToMenu and numberPlayers != keyToExit:
            playerNames, playerScores, playersAliveInGame = askNamePlayers(numberPlayers, normalGameInitialScore, keyBackToMenu, keyToExit)
            if playerNames == False:
                programExit = True
        elif numberPlayers == keyToExit:
            programExit = True
    elif optionSelected == 2:
        numberPlayers = askNumberPlayers(maxNumberPlayers, keyBackToMenu, keyToExit)
        if numberPlayers != keyBackToMenu and numberPlayers != keyToExit:
            playerNames, playerScores, playersAliveInGame = askNamePlayers(numberPlayers, normalGameInitialScore, keyBackToMenu, keyToExit)
            if playerNames == False:
                programExit = True
        elif numberPlayers == keyToExit:
            programExit = True
    elif optionSelected == 3:
        numberPlayers = askNumberPlayers(maxNumberPlayers, keyBackToMenu, keyToExit)
        if numberPlayers != keyBackToMenu and numberPlayers != keyToExit:
            playerNames, playerScores, playersAliveInGame = askNamePlayers(numberPlayers, normalGameInitialScore, keyBackToMenu, keyToExit)
            if playerNames == False:
                programExit = True
        elif numberPlayers == keyToExit:
            programExit = True
    elif optionSelected == 4:
        numberPlayers = askNumberPlayers(maxNumberPlayers, keyBackToMenu, keyToExit)
        if numberPlayers != keyBackToMenu and numberPlayers != keyToExit:
            playerNames, playerScores, playersAliveInGame = askNamePlayers(numberPlayers, normalGameInitialScore, keyBackToMenu, keyToExit)
            if playerNames == False:
                programExit = True
        elif numberPlayers == keyToExit:
            programExit = True
    elif optionSelected == 5:
        programExit = True