import random
import time

maxNumberPlayers = 5 #Maximum number of players allowed in any game mode
keyBackToMenu = "-" #With this answer, if a game hasn't started, the user may come back to menu
keyToExit = "+" #With this answer, if a game hasn't started, the user may exit the game
answerPossibleValues = ["YES", "NO"] #With these possible answers, the game validates whether a player believes to its previous player or not

normalGameInitialScore = 10 #Number of initial points for all players, in a normal game
normalScorePenalty = {42 : 3, 21 : 2} #With these special penalties, a player loses some points in a normal game, in other case, the player loses only one point
specialDiceValues = {66: "Sechser-Pasch", 55: "Fünfer-Pasch", 44: "Vierer-Pasch", 42: "Hamburger", 33: "Dreier-Pasch", 22: "Zweier-Pasch", 21: "Mäxchen", 11: "Einer-Pasch"} #Some dice values have special names

chanceRevealGeneratedNumber = 0.35 #Probability of a player cheats its turn (Knowing somehow the number generated)
chanceRevealPlayerSaysRightNumberOrNot = 0.35 #Probability of a player cheats its turn (Knowing somehow whether it believes in the answer given by the previous player or not)

chanceChangeTurnDirection = 0.35 #Probability of change the turns' order/direction (Just like in the UNO's game but with some probability rather than a card)

#It shows the main menu
def showMenu():
    print("Welcome to the Game")
    print("Please select and option:")
    print("1. Normal Game")
    print("2. Scoring Modified Game")
    print("3. Game with Trap")
    print("4. Game with Reverse Turn Directions")
    print("5. Exit")

#It shows the question to ask the number of players
def showNumberPlayersQuestion(maxNumberPlayers, keyBackToMenu, keyToExit):
    print("Indicate the number of players for the game. Minimum", 2, "and Maximum", maxNumberPlayers)
    print("Use the value", keyBackToMenu, "to go back to main menu")
    print("Use the value", keyToExit, "to quit the game")

#It shows the question to ask the name of a player (Only the name for one player)
def showNamePlayerQuestion(numberPlayer, keyBackToMenu, keyToExit):
    print("Indicate the name for the player", numberPlayer)
    print("Use the value", keyBackToMenu, "to go back to main menu")
    print("Use the value", keyToExit, "to quit the game")

#It shows the number of gamble (Gamble #1, Gamble #2, ...) and the player's name to the correspondent turn
def showNumberTurn(namePlayer, numberGambles):
    print("Gamble", numberGambles)
    if numberGambles == 1:
        print("The first turn is for the player", namePlayer)
    else:
        print("The turn is for the player", namePlayer)

#It shows the question to ask the player about the number generated
def showQuestionAboutNumberGenerated(namePlayer):
    print("The turn is for the player", namePlayer)
    print("Please, indicate the number generated.")

#It shows the question to ask the player whether it believes the answer given by the previous player or not
def showQuestionAboutAgreementAboutNumberIndicated(namePlayer):
    print("Question for the player", namePlayer)
    print("Do you believe that the number generated is right?")

#It shows the gamble's result (Number generated, Number given and the player who loses points)
def showAnswerAboutAgreementOrNoAgreement(nameLierPlayer, numberPointsLost, numberGenerated, numberProposed):
    print("Surprise!!!")
    print("Number Generated:", numberGenerated)
    print("Number Proposed", numberProposed)
    print("The player", nameLierPlayer, "loses", numberPointsLost, "points")

def showTurnOrderDirection(turnDirectionNormal):
    if turnDirectionNormal == True:
        print("The turns' order changes to Forward")
    else:
        print("The turns' order changes to Backward")

#It "clears" the screen, actually it only prints a lot of line breaks
def fakeClearScreen():
    for numberLine in range(10):
        print("")

#In this function, the user will indicate a menu's option to select a game modality or exit
#This function returns the number of option selected at the menu
def askMenuOption():
    optionSelected = 0
    #The value given by the user will be validated to verify it's an integer number between 1 and 5 (There are 5 options) and to know the option selected without ambiguity
    while optionSelected not in range(1, 6):
        fakeClearScreen()
        showMenu()
        #It tries to extract the integer number given by user, if it isn't possible, the question will be repeated to ask a right value
        try:
            optionSelected = int(input("Option: "))
        except ValueError:
            optionSelected = 0
    return optionSelected

#In this function, the user will indicate the number of players for the game (It's possible the user wants to come back to menu or exit the game)
#This function returns the number of players for the game
def askNumberPlayers(maxNumberPlayers, keyBackToMenu, keyToExit):
    numberPlayers = 0
    #The value given by the user will be validated to verify it's an integer number between 2 (Minimum number of players) and maxNumberPlayers (Maximum number of players)
    while numberPlayers not in range(2, maxNumberPlayers + 1):
        fakeClearScreen()
        showNumberPlayersQuestion(maxNumberPlayers, keyBackToMenu, keyToExit)
        value = input("Value (Number of Players): ")
        #First, it checks whether the value given matches or not with the keys to come back to menu or exit the game
        if value != keyBackToMenu and value != keyToExit:
            #It tries to extract the integer number given by user, if it isn't possible, the question will be repeated to ask a right value
            try:
                numberPlayers = int(value)
            except ValueError:
                numberPlayers = 0
        else:
            numberPlayers = value
            break
    return numberPlayers

#In this function, the user will indicate the name of the players for the game (One by one). Also, this function will prepare the players' scores, player's namelist and a list to coctrol the players alive in the game (Is to say, the players that haven't lose the game)
#This function returns the player's scores, namelist and a boolean list to check the players in possibility of win the game (Players alive in the game)
def askNamePlayers(numberPlayers, normalGameInitialScore, keyBackToMenu, keyToExit):
    playerNames = []
    playerScores = {}
    playersAliveInGame = []
    #The user will give the players' names, but it's possible the user wants to come back to menu or exit the game
    for index in range(numberPlayers):
        fakeClearScreen()
        showNamePlayerQuestion(index + 1, keyBackToMenu, keyToExit)
        currentPlayerName = input("Value (Name of Player): ")
        if currentPlayerName == keyBackToMenu:
            #It's convenient to assume the values are an exceptional value, to recognize the user really wants to come back to menu rather than play the game
            playerNames = []
            playerScores = {}
            playersAliveInGame = []
            break
        elif currentPlayerName == keyToExit:
            #It's convenient to assume the values are an exceptional value, to recognize the user really wants to exit the game rather than play the game
            playerNames = False
            playerScores = False
            playersAliveInGame = False
            break
        else:
            #To have a warranty the players's names are all different, these name are preceeded by a number between 1 and number of players
            currentPlayerId = str(index + 1) + " - " + currentPlayerName
            playerNames.append(currentPlayerId)
            playerScores[currentPlayerId] = normalGameInitialScore
            playersAliveInGame.append(True)
    return playerNames, playerScores, playersAliveInGame

#In this function, a player will indicate the number it thinks was generated
#This function returns the number indicated by the player
def askNumberGenerated(playerSelected):
    numberIndicated = "NaN"
    #The value given by the user will be validated to verify it's an integer number
    while numberIndicated == "NaN":
        showQuestionAboutNumberGenerated(playerSelected)
        value = input("Value (Possible Number Generated): ")
        #It tries to extract the integer number given by user, if it isn't possible, the question will be repeated to ask a right value
        try:
            numberIndicated = int(value)
        except ValueError:
            continue
    return numberIndicated

#In this function, a player will indicate the number it thinks was generated. In this case, with certain chance, the player may know previously the generated number
#This function returns the number indicated by the player
def askNumberGeneratedWithPossibleTrap(playerSelected, chanceRevealGeneratedNumber, numberGenerated):
    numberIndicated = "NaN"
    #The value given by the user will be validated to verify it's an integer number
    while numberIndicated == "NaN":
        showQuestionAboutNumberGenerated(playerSelected)
        #Here, it verifies whether the player cheats in the gamble
        if random.uniform(0, 1) <= chanceRevealGeneratedNumber:
            print("By a gossip, some player discovered that the number generated is", numberGenerated)
        value = input("Value (Possible Number Generated): ")
        #It tries to extract the integer number given by user, if it isn't possible, the question will be repeated to ask a right value
        try:
            numberIndicated = int(value)
        except ValueError:
            continue
    return numberIndicated

#In this function, a player will indicate whether it believes the number generated by the previous player is right or not
#This function returns the answer indicated by the player
def askWhetherPlayerBelievesOrNot(answerPossibleValues, playerSelected):
    answer = ""
    #The value given by the user will be validated to verify it's according to the possible values (Yes/No)
    while answer not in answerPossibleValues:
        showQuestionAboutAgreementAboutNumberIndicated(playerSelected)
        answer = input("Value (Yes/No): ").upper()
    return answer

#In this function, a player will indicate whether it believes the number generated by the previous player is right or not. In this case, with certain chance, the player may know previously whether the previous player lied or not
#This function returns the answer indicated by the player
def askWhetherPlayerBelievesOrNotWithPossibleTrap(answerPossibleValues, playerSelected, chanceRevealGeneratedNumber, numberGenerated, numberProposed):
    answer = ""
    #The value given by the user will be validated to verify it's according to the possible values (Yes/No)
    while answer not in answerPossibleValues:
        showQuestionAboutAgreementAboutNumberIndicated(playerSelected)
        #Here, it verifies whether the player cheats in the gamble
        if random.uniform(0, 1) <= chanceRevealGeneratedNumber:
            if numberProposed <= numberGenerated:
                print("By a gossip, some player discovered that you should believe it")
            else:
                print("By a gossip, some player discovered that you shouldn't believe it")
        answer = input("Value (Yes/No): ").upper()
    return answer

#In this function, it randomly will be selected the first player that starts the game
#This function returns the number of the selected player and its name
def selectFirstPlayer(playerNames, numberPlayers):
    numberSelected = random.randint(0, numberPlayers - 1)
    playerSelected = playerNames[numberSelected]
    return numberSelected, playerSelected

#In this function, it randomly will be selected a number generated by the roll of two dices (The dices may be of 6 faces or another number of faces). That number must verify that the first digit isn't less than the second digit
#This function returns the number generated by the dices
def getRollDices(numberDiceFaces):
    firstDigit = random.randint(1, numberDiceFaces)
    secondDigit = random.randint(1, numberDiceFaces)
    if firstDigit >= secondDigit:
        return 10 * firstDigit + secondDigit
    else:
        return 10 * secondDigit + firstDigit

#In this function, it determines the next player for perform the next gamble (That next player must be alive in the game)
#This function returns the player's number (Between 0 and numberPlayers - 1) and its name
def getNextPlayer(playerNames, playersAliveInGame, numberPlayers, currentPlayerNumber):
    numberNextPlayer = (currentPlayerNumber + 1) % numberPlayers #It will give an integer number between 0 and numberPlayers - 1 and it respect the turns' order
    nameNextPlayer = playerNames[numberNextPlayer]
    #The next player must be alive in the game, that validation is made here
    while playersAliveInGame[numberNextPlayer] == False:
        numberNextPlayer = (numberNextPlayer + 1) % numberPlayers
        nameNextPlayer = playerNames[numberNextPlayer]
    return numberNextPlayer, nameNextPlayer

#In this function, it determines the previous player for perform the next gamble (That next player must be alive in the game)
#This function returns the player's number (Between 0 and numberPlayers - 1) and its name
def getPreviousPlayer(playerNames, playersAliveInGame, numberPlayers, currentPlayerNumber):
    numberNextPlayer = (currentPlayerNumber - 1) % numberPlayers #It will give an integer number between 0 and numberPlayers - 1 and it respect the turns' order
    nameNextPlayer = playerNames[numberNextPlayer]
    #The next player must be alive in the game, that validation is made here
    while playersAliveInGame[numberNextPlayer] == False:
        numberNextPlayer = (numberNextPlayer - 1) % numberPlayers
        nameNextPlayer = playerNames[numberNextPlayer]
    return numberNextPlayer, nameNextPlayer

#In this function, the gamble is checked (It determines the player who said the truth and the player that lied, computes the score penalty for the lier player, updates the scores and checks whether a player is out of the game)
#This function returns updating of the players' scores, the list of players alive in the game and the number of players alive in the game
def checkGamble(playerScores, scorePenalty, playerNames, playersAliveInGame, numberPreviousPlayer, numberCurrentPlayer, numberPlayersAlive, numberGenerated, numberProposed):
    newPlayerScores = playerScores
    newPlayersAliveInGame = playersAliveInGame
    newNumberPlayers = numberPlayersAlive
    #Here, it determines the player that lied
    if numberProposed <= numberGenerated:
        lierPlayer = playerNames[numberCurrentPlayer]
    else:
        lierPlayer = playerNames[numberPreviousPlayer]
    #Here, it determines the score penalty before the player that lied loses points
    pointsLost = 0
    if numberProposed in scorePenalty.keys():
        pointsLost = scorePenalty[numberProposed]
    else:
        pointsLost = 1
    #Here, the player loses the points and the gamble's result is shown
    newPlayerScores[lierPlayer] -= pointsLost
    fakeClearScreen()
    showAnswerAboutAgreementOrNoAgreement(lierPlayer, pointsLost, numberGenerated, numberProposed)
    #Here, it determines if the player that lied is out of the game according to its new score
    if newPlayerScores[lierPlayer] <= 1:
        if numberProposed <= numberGenerated:
            newPlayersAliveInGame[numberCurrentPlayer] = False
        else:
            newPlayersAliveInGame[numberPreviousPlayer] = False
        newNumberPlayers -= 1
        print("The player", lierPlayer, "is out of the game")
    return newPlayerScores, newPlayersAliveInGame, newNumberPlayers

#In this function, it determines the player that won the game, it may be known according to the players alive in the game (The last player alive wins the game)
#This function returns the winner players's name
def getPlayerWinner(playerNames, playersAliveInGame):
    numberWinnerPlayer = playersAliveInGame.index(True) #It determines the winner player's number (Like the other players lost, there is only a value in the list with the boolean True value)
    return playerNames[numberWinnerPlayer]

#The program will end until the player wants to exit
programExit = False
while programExit == False:
    optionSelected = askMenuOption()
    #Option 1: Normal Game
    if optionSelected == 1:
        #Before the game starts, it has to know the number of players and its names (The user may come back to menu or exit the game)
        numberPlayers = askNumberPlayers(maxNumberPlayers, keyBackToMenu, keyToExit)
        if numberPlayers != keyBackToMenu and numberPlayers != keyToExit:
            playerNames, playerScores, playersAliveInGame = askNamePlayers(numberPlayers, normalGameInitialScore, keyBackToMenu, keyToExit)
            numberPlayersAlive = numberPlayers
            #If the user indicated the key to exit, the program ends
            if playerNames == False:
                programExit = True
            else:
                #Here the game starts
                numberGambles = 1
                fakeClearScreen()
                print("The game is going to start. Press enter to continue.")
                input("Value (Press Enter):")
                #The first player is selected randomly to start the game
                numberPlayerSelected, playerSelected = selectFirstPlayer(playerNames, numberPlayers)
                #The game will end until there is only a player alive
                while numberPlayersAlive > 1:
                    #Here, it's generated randomly a number according to the dices and it will be visible by two seconds
                    fakeClearScreen()
                    showNumberTurn(playerSelected, numberGambles)
                    numberGenerated = getRollDices(6)
                    print("You get the number", numberGenerated)
                    time.sleep(2)
                    #Here, the game asks the player to indicate the number it thinks was generated
                    fakeClearScreen()
                    numberProposed = askNumberGenerated(playerSelected)
                    #Here, the next player will indicated whether it believes the answer given by the previous player or not
                    fakeClearScreen()
                    numberPreviousPlayer = numberPlayerSelected
                    previousPlayer = playerSelected
                    numberPlayerSelected, playerSelected = getNextPlayer(playerNames, playersAliveInGame, numberPlayers, numberPlayerSelected)
                    answerQuestion = askWhetherPlayerBelievesOrNot(answerPossibleValues, playerSelected)
                    #Here, the gamble is checked to determine the player that said the truth and the player that lied (Only if the next player tells not believes the answer given), and also, the scores are updated and it checks whether the lier player is out of the game
                    if answerQuestion == answerPossibleValues[1]:
                        playerScores, playersAliveInGame, numberPlayersAlive = checkGamble(playerScores, normalScorePenalty, playerNames, playersAliveInGame, numberPreviousPlayer, numberPlayerSelected, numberPlayersAlive, numberGenerated, numberProposed)
                        numberPlayerSelected, playerSelected = getNextPlayer(playerNames, playersAliveInGame, numberPlayers, numberPlayerSelected)
                    #Here, it shows the scores updated and the players alive in the game
                    print("Scores:", playerScores)
                    print("List of Players Alive:", playersAliveInGame)
                    print("Number of Players Alive:", numberPlayersAlive)
                    numberGambles += 1
                    #Here, it determines whether the game continues or is over
                    if numberPlayersAlive > 1:
                        print("The next gamble is going to start. Press enter to continue.")
                        input("Value (Press Enter):")
                    else:
                        print("The game is finished.")
                        nameWinnerPlayer = getPlayerWinner(playerNames, playersAliveInGame)
                        print("The winner is", nameWinnerPlayer, "with", playerScores[nameWinnerPlayer], "points")
                        print("All Scores:", playerScores)
                        print("Number Gambles:", numberGambles)
                        print("Press enter to continue.")
                        input("Value (Press Enter):")
        #If the user indicated the key to exit, the program ends
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
    #Option 3: Game with chance of cheats
    elif optionSelected == 3:
        #Before the game starts, it has to know the number of players and its names (The user may come back to menu or exit the game)
        numberPlayers = askNumberPlayers(maxNumberPlayers, keyBackToMenu, keyToExit)
        if numberPlayers != keyBackToMenu and numberPlayers != keyToExit:
            playerNames, playerScores, playersAliveInGame = askNamePlayers(numberPlayers, normalGameInitialScore, keyBackToMenu, keyToExit)
            numberPlayersAlive = numberPlayers
            #If the user indicated the key to exit, the program ends
            if playerNames == False:
                programExit = True
            else:
                #Here the game starts
                numberGambles = 1
                fakeClearScreen()
                print("The game is going to start. Press enter to continue.")
                input("Value (Press Enter):")
                #The first player is selected randomly to start the game
                numberPlayerSelected, playerSelected = selectFirstPlayer(playerNames, numberPlayers)
                #The game will end until there is only a player alive
                while numberPlayersAlive > 1:
                    #Here, it's generated randomly a number according to the dices and it will be visible by two seconds
                    fakeClearScreen()
                    showNumberTurn(playerSelected, numberGambles)
                    numberGenerated = getRollDices(6)
                    print("You get the number", numberGenerated)
                    time.sleep(2)
                    #Here, the game asks the player to indicate the number it thinks was generated
                    fakeClearScreen()
                    #numberProposed = askNumberGenerated(playerSelected) #It changes in this case (Compared with the Normal Game), to include the possible cheat by the player
                    numberProposed = askNumberGeneratedWithPossibleTrap(playerSelected, chanceRevealGeneratedNumber, numberGenerated)
                    #Here, the next player will indicated whether it believes the answer given by the previous player or not
                    fakeClearScreen()
                    numberPreviousPlayer = numberPlayerSelected
                    previousPlayer = playerSelected
                    numberPlayerSelected, playerSelected = getNextPlayer(playerNames, playersAliveInGame, numberPlayers, numberPlayerSelected)
                    #answerQuestion = askWhetherPlayerBelievesOrNot(answerPossibleValues, playerSelected) #It changes in this case (Compared with the Normal Game), to include the possible cheat by the player
                    answerQuestion = askWhetherPlayerBelievesOrNotWithPossibleTrap(answerPossibleValues, playerSelected, chanceRevealPlayerSaysRightNumberOrNot, numberGenerated, numberProposed)
                    #Here, the gamble is checked to determine the player that said the truth and the player that lied (Only if the next player tells not believes the answer given), and also, the scores are updated and it checks whether the lier player is out of the game
                    if answerQuestion == answerPossibleValues[1]:
                        playerScores, playersAliveInGame, numberPlayersAlive = checkGamble(playerScores, normalScorePenalty, playerNames, playersAliveInGame, numberPreviousPlayer, numberPlayerSelected, numberPlayersAlive, numberGenerated, numberProposed)
                        numberPlayerSelected, playerSelected = getNextPlayer(playerNames, playersAliveInGame, numberPlayers, numberPlayerSelected)
                    #Here, it shows the scores updated and the players alive in the game
                    print("Scores:", playerScores)
                    print("List of Players Alive:", playersAliveInGame)
                    print("Number of Players Alive:", numberPlayersAlive)
                    numberGambles += 1
                    #Here, it determines whether the game continues or is over
                    if numberPlayersAlive > 1:
                        print("The next gamble is going to start. Press enter to continue.")
                        input("Value (Press Enter):")
                    else:
                        print("The game is finished.")
                        nameWinnerPlayer = getPlayerWinner(playerNames, playersAliveInGame)
                        print("The winner is", nameWinnerPlayer, "with", playerScores[nameWinnerPlayer], "points")
                        print("All Scores:", playerScores)
                        print("Number Gambles:", numberGambles)
                        print("Press enter to continue.")
                        input("Value (Press Enter):")
        #If the user indicated the key to exit, the program ends
        elif numberPlayers == keyToExit:
            programExit = True
    #Option 4: Game with chance of change the turn's order
    elif optionSelected == 4:
        #Before the game starts, it has to know the number of players and its names (The user may come back to menu or exit the game)
        numberPlayers = askNumberPlayers(maxNumberPlayers, keyBackToMenu, keyToExit)
        if numberPlayers != keyBackToMenu and numberPlayers != keyToExit:
            playerNames, playerScores, playersAliveInGame = askNamePlayers(numberPlayers, normalGameInitialScore, keyBackToMenu, keyToExit)
            numberPlayersAlive = numberPlayers
            #If the user indicated the key to exit, the program ends
            if playerNames == False:
                programExit = True
            else:
                #Here the game starts
                numberGambles = 1
                turnDirectionNormal = True #The turns' order starts normally (True: From the first randomly selected player forward, False: From the first randomly selected player backward)
                fakeClearScreen()
                print("The game is going to start. Press enter to continue.")
                input("Value (Press Enter):")
                #The first player is selected randomly to start the game
                numberPlayerSelected, playerSelected = selectFirstPlayer(playerNames, numberPlayers)
                #The game will end until there is only a player alive
                while numberPlayersAlive > 1:
                    #Here, it's generated randomly a number according to the dices and it will be visible by two seconds
                    fakeClearScreen()
                    showNumberTurn(playerSelected, numberGambles)
                    numberGenerated = getRollDices(6)
                    print("You get the number", numberGenerated)
                    time.sleep(2)
                    #Here, the game asks the player to indicate the number it thinks was generated
                    fakeClearScreen()
                    numberProposed = askNumberGenerated(playerSelected)
                    #Here, the next player will indicated whether it believes the answer given by the previous player or not
                    fakeClearScreen()
                    numberPreviousPlayer = numberPlayerSelected
                    previousPlayer = playerSelected
                    #Here, it applies a chance to change the turns' order
                    if random.uniform(0, 1) < chanceChangeTurnDirection:
                        turnDirectionNormal = not turnDirectionNormal #This value inverts it (If the value was True, then the value will be False and vice versa)
                        showTurnOrderDirection(turnDirectionNormal)
                        print("Press enter to continue.")
                        input("Value (Press Enter):")
                        fakeClearScreen()
                    #According to turns' order, the next player (This player will answer whether believes the number indicated by the player or not) will be (True: One step forward to players' list, False: One step backward to players' list)
                    if turnDirectionNormal == True:
                        numberPlayerSelected, playerSelected = getNextPlayer(playerNames, playersAliveInGame, numberPlayers, numberPlayerSelected)
                    else:
                        numberPlayerSelected, playerSelected = getPreviousPlayer(playerNames, playersAliveInGame, numberPlayers, numberPlayerSelected)
                    answerQuestion = askWhetherPlayerBelievesOrNot(answerPossibleValues, playerSelected)
                    #Here, the gamble is checked to determine the player that said the truth and the player that lied (Only if the next player tells not believes the answer given), and also, the scores are updated and it checks whether the lier player is out of the game
                    if answerQuestion == answerPossibleValues[1]:
                        playerScores, playersAliveInGame, numberPlayersAlive = checkGamble(playerScores, normalScorePenalty, playerNames, playersAliveInGame, numberPreviousPlayer, numberPlayerSelected, numberPlayersAlive, numberGenerated, numberProposed)
                        #Here, it applies a chance to change the turns' order
                        if random.uniform(0, 1) < chanceChangeTurnDirection:
                            turnDirectionNormal = not turnDirectionNormal #This value inverts it (If the value was True, then the value will be False and vice versa)
                            showTurnOrderDirection(turnDirectionNormal)
                            print("Press enter to continue.")
                            input("Value (Press Enter):")
                            fakeClearScreen()
                        #According to turns' order, the next player (This player will roll the dices) will be (True: One step forward to players' list, False: One step backward to players' list)
                        if turnDirectionNormal == True:
                            numberPlayerSelected, playerSelected = getNextPlayer(playerNames, playersAliveInGame, numberPlayers, numberPlayerSelected)
                        else:
                            numberPlayerSelected, playerSelected = getPreviousPlayer(playerNames, playersAliveInGame, numberPlayers, numberPlayerSelected)
                    #Here, it shows the scores updated and the players alive in the game
                    print("Scores:", playerScores)
                    print("List of Players Alive:", playersAliveInGame)
                    print("Number of Players Alive:", numberPlayersAlive)
                    numberGambles += 1
                    #Here, it determines whether the game continues or is over
                    if numberPlayersAlive > 1:
                        print("The next gamble is going to start. Press enter to continue.")
                        input("Value (Press Enter):")
                    else:
                        print("The game is finished.")
                        nameWinnerPlayer = getPlayerWinner(playerNames, playersAliveInGame)
                        print("The winner is", nameWinnerPlayer, "with", playerScores[nameWinnerPlayer], "points")
                        print("All Scores:", playerScores)
                        print("Number Gambles:", numberGambles)
                        print("Press enter to continue.")
                        input("Value (Press Enter):")
        #If the user indicated the key to exit, the program ends
        elif numberPlayers == keyToExit:
            programExit = True
    elif optionSelected == 5:
        programExit = True