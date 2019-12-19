import sys
import random
import time

maxNumberPlayers = 5
keyBackToMenu = "-"
keyToExit = "+"
answerPossibleValues = ["YES", "NO"]

normalGameInitialScore = 10
normalScorePenalty = {42 : 3, 21 : 2}
specialDiceValues = {66: "Sechser-Pasch", 55: "Fünfer-Pasch", 44: "Vierer-Pasch", 42: "Hamburger", 33: "Dreier-Pasch", 22: "Zweier-Pasch", 21: "Mäxchen", 11: "Einer-Pasch"}

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

def showNamePlayerQuestion(numberPlayer, keyBackToMenu, keyToExit):
    print("Indicate the name for the player", numberPlayer)
    print("Use the value", keyBackToMenu, "to go back to main menu")
    print("Use the value", keyToExit, "to quit the game")

def showNumberTurn(namePlayer, numberGambles):
    print("Gamble", numberGambles)
    if numberGambles == 1:
        print("The first turn is for the player", namePlayer)
    else:
        print("The turn is for the player", namePlayer)

def showQuestionAboutNumberGenerated(namePlayer):
    print("The turn is for the player", namePlayer)
    print("Please, indicate the number generated.")

def showQuestionAboutAgreementAboutNumberIndicated(namePlayer):
    print("Question for the player", namePlayer)
    print("Do you believe that the number generated is right?")

def showAnswerAboutAgreementOrNoAgreement(nameLierPlayer, numberPointsLost, numberGenerated, numberProposed):
    print("Surprise!!!")
    print("Number Generated:", numberGenerated)
    print("Number Proposed", numberProposed)
    print("The player", nameLierPlayer, "loses", numberPointsLost, "points")

def fakeClearScreen():
    for numberLine in range(10):
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
        showNamePlayerQuestion(index + 1, keyBackToMenu, keyToExit)
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

def askNumberGenerated(playerSelected):
    numberIndicated = "NaN"
    while numberIndicated == "NaN":
        showQuestionAboutNumberGenerated(playerSelected)
        print("Value:")
        value = sys.stdin.readline().strip()
        try:
            numberIndicated = int(value)
        except ValueError:
            continue
    return numberIndicated

def askWhetherPlayerBelievesOrNot(answerPossibleValues, playerSelected):
    answer = ""
    while answer not in answerPossibleValues:
        showQuestionAboutAgreementAboutNumberIndicated(playerSelected)
        print("Value:")
        answer = sys.stdin.readline().strip().upper()
    return answer

def selectFirstPlayer(playerNames, numberPlayers):
    numberSelected = random.randint(0, numberPlayers - 1)
    playerSelected = playerNames[numberSelected]
    return numberSelected, playerSelected

def getRollDices(numberDiceFaces):
    firstDigit = random.randint(1, numberDiceFaces)
    secondDigit = random.randint(1, numberDiceFaces)
    if firstDigit >= secondDigit:
        return 10 * firstDigit + secondDigit
    else:
        return 10 * secondDigit + firstDigit

def getNextPlayer(playerNames, playersAliveInGame, numberPlayers, currentPlayerNumber):
    numberNextPlayer = (currentPlayerNumber + 1) % numberPlayers
    nameNextPlayer = playerNames[numberNextPlayer]
    while playersAliveInGame[numberNextPlayer] == False:
        numberNextPlayer = (numberNextPlayer + 1) % numberPlayers
        nameNextPlayer = playerNames[numberNextPlayer]
    return numberNextPlayer, nameNextPlayer

def checkGamble(playerScores, scorePenalty, playerNames, playersAliveInGame, numberPreviousPlayer, numberCurrentPlayer, numberPlayersAlive, numberGenerated, numberProposed):
    newPlayerScores = playerScores
    newPlayersAliveInGame = playersAliveInGame
    newNumberPlayers = numberPlayersAlive
    if numberProposed <= numberGenerated:
        lierPlayer = playerNames[numberCurrentPlayer]
    else:
        lierPlayer = playerNames[numberPreviousPlayer]
    pointsLost = 0
    if numberProposed in scorePenalty.keys():
        pointsLost = scorePenalty[numberProposed]
    else:
        pointsLost = 1
    newPlayerScores[lierPlayer] -= pointsLost
    showAnswerAboutAgreementOrNoAgreement(lierPlayer, pointsLost, numberGenerated, numberProposed)
    if newPlayerScores[lierPlayer] <= 1:
        if numberProposed <= numberGenerated:
            newPlayersAliveInGame[numberCurrentPlayer] = False
        else:
            newPlayersAliveInGame[numberPreviousPlayer] = False
        newNumberPlayers -= 1
        print("The player", lierPlayer, "is out of the game")
    return newPlayerScores, newPlayersAliveInGame, newNumberPlayers

def getPlayerWinner(playerNames, playersAliveInGame):
    numberWinnerPlayer = playersAliveInGame.index(True)
    return playerNames[numberWinnerPlayer]

programExit = False
while programExit == False:
    optionSelected = askMenuOption()
    if optionSelected == 1:
        numberPlayers = askNumberPlayers(maxNumberPlayers, keyBackToMenu, keyToExit)
        if numberPlayers != keyBackToMenu and numberPlayers != keyToExit:
            playerNames, playerScores, playersAliveInGame = askNamePlayers(numberPlayers, normalGameInitialScore, keyBackToMenu, keyToExit)
            numberPlayersAlive = numberPlayers
            if playerNames == False:
                programExit = True
            else:
                numberGambles = 1
                fakeClearScreen()
                print("The game is going to start. Press enter to continue.")
                print("Value:")
                sys.stdin.readline().strip()
                numberPlayerSelected, playerSelected = selectFirstPlayer(playerNames, numberPlayers)
                while numberPlayersAlive > 1:
                    fakeClearScreen()
                    showNumberTurn(playerSelected, numberGambles)
                    numberGenerated = getRollDices(6)
                    print("You get the number", numberGenerated)
                    time.sleep(2)
                    fakeClearScreen()
                    numberProposed = askNumberGenerated(playerSelected)
                    fakeClearScreen()
                    numberPreviousPlayer = numberPlayerSelected
                    previousPlayer = playerSelected
                    numberPlayerSelected, playerSelected = getNextPlayer(playerNames, playersAliveInGame, numberPlayers, numberPlayerSelected)
                    answerQuestion = askWhetherPlayerBelievesOrNot(answerPossibleValues, playerSelected)
                    if answerQuestion == answerPossibleValues[1]:
                        playerScores, playersAliveInGame, numberPlayersAlive = checkGamble(playerScores, normalScorePenalty, playerNames, playersAliveInGame, numberPreviousPlayer, numberPlayerSelected, numberPlayersAlive, numberGenerated, numberProposed)
                        numberPlayerSelected, playerSelected = getNextPlayer(playerNames, playersAliveInGame, numberPlayers, numberPlayerSelected)
                    print("Scores: ", playerScores)
                    print(playersAliveInGame)
                    print(numberPlayersAlive)
                    numberGambles += 1
                    if numberPlayersAlive > 1:
                        print("The next gamble is going to start. Press enter to continue.")
                        print("Value:")
                        sys.stdin.readline().strip()
                    else:
                        print("The game is finished.")
                        nameWinnerPlayer = getPlayerWinner(playerNames, playersAliveInGame)
                        print("The winner is", nameWinnerPlayer, "with", playerScores[nameWinnerPlayer], "points")
                        print("All Scores:", playerScores)
                        print("Number Gambles:", numberGambles)
                        print("Press enter to continue.")
                        print("Value:")
                        sys.stdin.readline().strip()
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