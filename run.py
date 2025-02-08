
import json
import random
from time import sleep
import colorama

#Initialize Colorama
colorama.init()



class Player:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        
#Saves correct guessed Letters in a List
guessedCorrectLetters = []
#Saves incorrect guessed Letters in a List
guessedIncorrectLetters = []
#Get Random Instace for Word and Tip
randomInstance = random.randint(0,150)

def fetchWord(file):
        """Fetch a random word"""
        word = file[randomInstance]["word"].lower()
        return word    

def fetchTip(file):
    """Fetch the definition of the random word"""
    tip = file[randomInstance]["tip"]
    return tip

def fetchLanguageFilePath(language):
    """Fetch correct file path corresponding to chosen language"""
    if language == "de":
        filePath = "assets/json/de-words.json"
        print("Du hast Deutsch gewählt\n")
        return filePath
    elif language == "du":
        filePath = "assets/json/du-words.json"
        print("Je hebt Nederlands gekozen\n")
        return filePath
    else:
        filePath = "assets/json/en-words.json"
        print("You chose english\n")
        return filePath

def fetchFile(filePath):
    with open(filePath, "r") as file:
            words = json.load(file)
    return words

def letPlayerChooseLanguage():
    """Let user choose his language to play in"""
    print("\nYou can chosse between different languages to play in.")
    language = input("Write 'de' for german, 'du' for dutch. Just english just press Enter: ")

    if language == "de" or language == "du" or language == "":
        return language
    else:
        print("Please select a language or press enter")
        return letPlayerChooseLanguage()

def letPlayerGuessLetter(file):
    """Let the player enter a guessed letter"""
    print("Guess one letter. Write 'help' for a tip or 'quit' to exit the game")

    guess = input("Your guess: ").lower()

    if not guess.isalpha():
        print("Only letters are allowed")
        sleep(2)
        return letPlayerGuessLetter(file)
    if guess == "help":
        help = fetchTip(file)
        print(help)
        sleep(2)
        return letPlayerGuessLetter(file)
    if guess == "quit":
        quit()

    if len(guess) > 1:
        print("You can guess only one letter")
        sleep(2)
        return letPlayerGuessLetter(file)
    else:
        return guess

def printTutorial():
    """Write a tutorial to display at the start of the game"""

    print("\nWelcome to Hangman\n")
    print("How to play:\n")
    print("A secret word is chosen. Each underscore represents one secret letter.")
    print("Guess one letter at a time. If the letter is in the word, its position(s) will be reveal.")
    print("If the letter is incorrect, you lose one of your guess chances.")
    print("If you need help, write 'help' to get a tip.")
    print("Win: All letters are revealed.")
    print("Lose: The full hangman drawing is finished before the word is guessed.\n")

def fetchPlayerName():
    """Let the user name himself for a more immersiv experience"""
    name = input("Enter your Name to start the game: ").capitalize()
    if not name.isalpha():
        print("Please enter only letters\n")
        return fetchPlayerName()
    else:
        return name

def fetchCustomDifficulty():
    """Let the user decide how many guesses he wants to have"""
    try:
        customGuesses = int(input("Enter the number of guesses you want to start the game with (1 - 12). The more guesses the easier the game gets: "))
        if customGuesses < 1 or customGuesses > 12:
            print("You cant do that. Lowest possible input is 1 and highest is 12.")
            return fetchCustomDifficulty()
    except ValueError:
        print("Only numbers are allowed")
        return fetchCustomDifficulty()
    
    return customGuesses
    
def createPlayer(playerName, playerGuesses):
    """Create new Player instance"""
    newPlayer = Player(playerName, playerGuesses)
    return newPlayer

def displayLetterCount(word, guessedCorrectLetters):
    """Display the amount of letters the word has as underlines"""
    combinedLetters = []
    if len(guessedCorrectLetters) == 0:
        print(" ".join(["_" for letter in word]))
    else: #Merge guessed Letters and missing letters
        for letter in word:
            if letter in guessedCorrectLetters:
                combinedLetters.append(letter)
            else:
                combinedLetters.append("_")
        print(" ".join(combinedLetters))

def displayAlreadyGuessedLetters(wrongLetters):
    """Display the already guessed Letters after each guess"""
    if wrongLetters:
        wrongLetterList = ", ".join(wrongLetters)
        print(f"You already guessed: {wrongLetterList}")

def checkForAlreadyGuessedLetter(guess, correctGuesses, incorrectGuesses, file):
    """Check the guess of the user and remind him of already guessed letters"""
    if guess in correctGuesses or guess in incorrectGuesses:
        print("You already guessed that letter. Try again")
        return letPlayerGuessLetter(file)
    else:
        return guess

def checkIfAnwserIsCorrect(guess, word):
    """Check if the guessed letter can be found within the word"""
    safeValidation = []
    for letter in word:
        if guess == letter:
            safeValidation.append(1)
        else:
            pass
    #If no letter was correct it returns an empty list wich is == to False
    return safeValidation

def reducePlayerHealth(letterValidation, player):
    """Reduces Player health depending on right or wrong guess"""
    if letterValidation:
        return
    
    player.health -=1
    
def appendLetterIntoList(letterValidation, guess):
    if letterValidation:
        guessedCorrectLetters.append(guess)
    else:
        guessedIncorrectLetters.append(guess)

def displayGuessConfirmation(guessletterValidation, player):
    """Display to the User if his guess was correct or incorrect"""
    if guessletterValidation:
        print("You guessed correct!")
    else:
        if player.health > 1:
            print(f"Incorrect. You have {player.health} trys left")
        else:
            return
        
def askForAnotherRound():
    """Ask the player if he wants to play another round"""
    userChoice = input("Do you want to play again. Type 'y' for another round and 'n' to quit the program: ").lower()
    if not userChoice.isalpha():
        print("Please type 'y' or 'n'")
        return askForAnotherRound()
    elif  userChoice == "y" or userChoice == "n":
        return userChoice
    else:
        print("Please type 'y' or 'n'")
        return askForAnotherRound()
        
def checkForGameEnd(player, word, correctGuesses):
    """Checks if the player did win or lose yet"""
    if player.health < 1 or set(correctGuesses) == set(word):
        return True    

def endGame(choice):
    if choice == "y":
        global gameLoop
        main()
    else:
        quit()

def displayGameOver(player, word):
    """Display an individual message depending in the loss or win of the player"""
    if player.health == 0:
        print(f"You lost! The word would have been '{word}'.")
    else:
        print(f"You won and you still had {player.health} trys left. Good job")

def resetGlobalVariables():
    """Reset global Variables such as guessed Letters and so on"""
    global guessedCorrectLetters
    global guessedIncorrectLetters
    global randomInstance

    guessedCorrectLetters = []
    guessedIncorrectLetters = []
    randomInstance = random.randint(0,150)
def main():
    resetGlobalVariables()
    printTutorial()
    sleep(1)
    playerName = fetchPlayerName()
    language = letPlayerChooseLanguage()
    filePath = fetchLanguageFilePath(language)
    file = fetchFile(filePath)
    playerHealth = fetchCustomDifficulty()
    player = createPlayer(playerName, playerHealth)
    word = fetchWord(file)
    print(word)
    while True:
        sleep(1)
        displayLetterCount(word, guessedCorrectLetters)
        if guessedIncorrectLetters:
            displayAlreadyGuessedLetters(guessedIncorrectLetters)
        sleep(1)
        guess = letPlayerGuessLetter(file)
        checkForAlreadyGuessedLetter(guess, guessedCorrectLetters, guessedIncorrectLetters, file)
        letterValidation = checkIfAnwserIsCorrect(guess, word)
        reducePlayerHealth(letterValidation, player)
        displayGuessConfirmation(letterValidation, player)
        appendLetterIntoList(letterValidation, guess)
        gameEndValidation = checkForGameEnd(player, word, guessedCorrectLetters)
        if gameEndValidation:
            displayGameOver(player, word)
            userChoice = askForAnotherRound()
            endGame(userChoice)


main()
