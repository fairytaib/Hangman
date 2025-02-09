#Import Json Functionalitys
import json
#Import Library for Random Selection
import random
#Import Sleep for better user experience
from time import sleep
#import Colorama for colors
import colorama
from colorama import Fore, Back, Style
#import Terminal Oprion Library
import inquirer

#Initialize Colorama
colorama.init(autoreset=True)

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
# Check if it is the first round
PLAYEREXISTS = False
# Keeps track if the Tip was bought already
BOUGHTTIP = False
#Create gobal Player varibale
player = None

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
    if language == "German":
        filePath = "assets/json/de-words.json"
        print("Du hast Deutsch gewählt\n")
        return filePath
    elif language == "Dutch":
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
    languageOptions = [
        inquirer.List('language',
                      message="Choose your language to play in",
                      choices=["English", "German", "Dutch", "Display Rules again","Quit"],
                      ),
    ]
    chosenLanguage = inquirer.prompt(languageOptions)
    
    if chosenLanguage['language'] == "Quit":
        print("\nGoodbye")
        quit()
    elif chosenLanguage['language'] == "Display Rules again":
        printTutorial() 
        sleep(2)
        return letPlayerChooseLanguage()

    return chosenLanguage
    
def letPlayerGuessLetter(file, player):
    """Let the player enter a guessed letter"""
    global BOUGHTTIP
    if player.health > 1 and BOUGHTTIP:
        print("Guess one letter. Type 'tip' to buy a tip for one of your health points or write 'quit' to exit the game")
    else:
        print("Guess one letter. Write 'quit' to exit the game")

    guess = input("Your guess: ").lower()

    if not guess.isalpha():
        print("Only letters are allowed")
        sleep(2)
        return letPlayerGuessLetter(file, player)
    if guess == "tip":
        help = fetchTip(file)
        print(f"You have now {player.health} trys left")
        player.health -= 1
        BOUGHTTIP = False
        print(help)
        sleep(2)
        return letPlayerGuessLetter(file,player)
    if guess == "quit":
        quit()

    if len(guess) > 1:
        print("You can guess only one letter")
        sleep(2)
        return letPlayerGuessLetter(file, player)
    else:
        return guess

def printWelcomeMessage():
    """Print Welcome Message"""
    #Seperated from tutorial message to call tutorial on different places of the game
    print("\nWelcome to Hangman!\n")

def printTutorial():
    """Write a tutorial to display at the start of the game"""

    print("How to play:\n")
    print("A secret word is chosen. Each underscore represents one secret letter.")
    print("Guess one letter at a time. If the letter is in the word, its position(s) will be reveal.")
    print("If the letter is incorrect, you lose one of your guess chances.")
    print("If you need help, write 'help' to get a tip.")
    print("Win: All letters are revealed.")
    print("Lose: The full hangman drawing is finished before the word is guessed.\n")

def fetchPlayerName():
    """Let the user name himself for a more immersiv experience"""
    name = input("Enter your Name to start the game or 'q' to end programm: ").capitalize()
    if not name.isalpha():
        print("Please enter only letters and no whitespace.\n")
        return fetchPlayerName()
    elif name == "Q":
        print("Goodbye")
        quit()
    else:
        return name

def fetchCustomDifficulty():
    """Let the user decide how many guesses he wants to have"""
    print("You can choose a custom difficulty. The harder you want the game to be, the less trys you will have.\n")
    print("Easy = 12 wrong guesses")
    print("Medium = 8 wrong guesses")
    print("Hard = 4 wrong guesses")
    print("Impossible = One wrong guess and you lose\n")
    difficultyOptions = [
        inquirer.List('difficulty',
                      message="Choose your difficulty",
                      choices=["Easy", "Medium", "Hard", "Impossible", "Leave Game"],
                      ),
    ]
    chosenDifficulty = inquirer.prompt(difficultyOptions)

    if chosenDifficulty["difficulty"] == "Easy":
        return 12
    elif chosenDifficulty["difficulty"] == "Medium":
        return 8
    elif chosenDifficulty["difficulty"] == "Hard":
        return 4
    elif chosenDifficulty["difficulty"] == "Impossible":
        return 1
    elif chosenDifficulty["difficulty"] == "Leave Game":
        print("Goodbye")
        quit()
  
def createPlayer(playerName, playerDifficulty):
    """Create new Player instance"""
    global PLAYEREXISTS
    newPlayer = Player(playerName, playerDifficulty)
    PLAYEREXISTS = True
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

def checkForAlreadyGuessedLetter(guess, correctGuesses, incorrectGuesses, file, player):
    """Check the guess of the user and remind him of already guessed letters"""
    if guess in correctGuesses or guess in incorrectGuesses:
        print("You already guessed that letter. Try again")
        return letPlayerGuessLetter(file, player)
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
    menuOptions = [
        inquirer.List('menu',
                      message="Do you want to play again",
                      choices=["Play again", "Leave Game"],
                      ),
    ]
    chosenMenu = inquirer.prompt(menuOptions)
    return chosenMenu["menu"]
        
def checkForGameEnd(player, word, correctGuesses):
    """Checks if the player did win or lose yet"""
    if player.health < 1 or set(correctGuesses) == set(word):
        return True    

def endGame(choice):
    if choice == "Play again":
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

def resetPlayerHealth(difficulty, player):
    """Reset Difficulty / player health after a round"""
    player.health = difficulty
    
def main():
    global player
    resetGlobalVariables()
    sleep(1)
    # Skip function if User already registered Name
    if PLAYEREXISTS:
        pass
    else:
        printTutorial()
        printTutorial()
        playerName = fetchPlayerName()
    language = letPlayerChooseLanguage()
    filePath = fetchLanguageFilePath(language)
    file = fetchFile(filePath)
    playerHealth = fetchCustomDifficulty()
    # Skip function if User already exists
    if not PLAYEREXISTS:
        player = createPlayer(playerName, playerHealth)
    else:
        resetPlayerHealth(playerHealth, player)
    word = fetchWord(file)
    print(word) #REMOVE LATER!!!!!!!!!!!!!!!!!!!!!!!!!!!
    while True:
        sleep(1)
        displayLetterCount(word, guessedCorrectLetters)
        if guessedIncorrectLetters:
            displayAlreadyGuessedLetters(guessedIncorrectLetters)
        sleep(1)
        guess = letPlayerGuessLetter(file, player)
        checkForAlreadyGuessedLetter(guess, guessedCorrectLetters, guessedIncorrectLetters, file, player)
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
