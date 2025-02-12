import json
import random
from time import sleep
# import Colorama for colors
import colorama
from colorama import Fore, Back, Style
# import Terminal Oprion Library
import inquirer

# Initialize Colorama
colorama.init(autoreset=True)


class Player:
    """ Creates a Player class to store individuel user 'information' """
    def __init__(self, name, health):
        self.name = name
        self.health = health


# Saves correct guessed Letters in a List
guessed_correct_letters = []
# Saves incorrect guessed Letters in a List
guessed_incorrect_letters = []
# Get Random Instace for Word and Tip
random_instance = random.randint(0, 150)
#  Check if it is the first round
PLAYEREXISTS = False
#  Keeps track if the Tip was bought already
TIPAVAILABLE = True
# Create gobal Player varibale
player = None


def fetch_word(file):
    """Fetch a random word"""
    word = file[random_instance]["word"].lower()
    return word


def fetch_tip(file):
    """Fetch the definition of the random word"""
    tip = file[random_instance]["tip"]
    return tip


def fetch_language_file_path(language):
    """Fetch correct file path corresponding to chosen language"""
    if language == "German":
        file_path = "assets/json/de-words.json"
        print(Fore.CYAN + "Du hast Deutsch gewählt\n")
        return file_path
    elif language == "Dutch":
        file_path = "assets/json/du-words.json"
        print(Fore.CYAN + "Je hebt Nederlands gekozen\n")
        return file_path
    else:
        file_path = "assets/json/en-words.json"
        print(Fore.CYAN + "You chose english\n")
        return file_path


def fetch_file(file_path):
    """Open file json file"""
    with open(file_path, "r") as file:
        words = json.load(file)
    return words


def let_player_choose_language():
    """Let user choose his language to play in"""
    language_options = [
        inquirer.List(
            'language',
            message=Fore.CYAN + "Choose the words language",
            choices=[
                Fore.YELLOW + "English",
                Fore.YELLOW + "German",
                Fore.YELLOW + "Dutch",
                Fore.YELLOW + "Display Rules again",
                Fore.RED + "Quit"]
        ),
    ]
    chosen_language = inquirer.prompt(language_options)

    if chosen_language['language'] == Fore.RED + "Quit":
        print(Fore.CYAN + "\nGoodbye")
        quit()
    elif chosen_language['language'] == Fore.YELLOW + "Display Rules again":
        print_tutorial()
        sleep(2)
        return let_player_choose_language()

    return chosen_language["language"]


def let_player_guess_letter(file, player):
    """Let the player enter a guessed letter"""
    global TIPAVAILABLE
    if player.health > 1 and TIPAVAILABLE:
        print(Fore.CYAN + "Guess one letter. Type 'tip' to buy a tip for"
              "one of your health points or write 'quit' to exit the game")
    elif not TIPAVAILABLE and player.health > 1:
        print(Fore.CYAN + "Guess one letter. Type 'tip' to review the"
              "tip or write 'quit' to exit the game")
    else:
        print(Fore.CYAN + "Guess one letter. Write 'quit' to exit the game")

    guess = input(Fore.CYAN + "Your guess: ").lower()

    if not guess.isalpha():
        print(Fore.RED + "Only letters are allowed")
        sleep(2)
        return let_player_guess_letter(file, player)
    if guess == "tip" and TIPAVAILABLE:
        help = fetch_tip(file)
        print(f"""{Fore.YELLOW} You bought a tip.
              {Fore.YELLOW} You have now {player.health} tries left.""")
        
        player.health -= 1
        TIPAVAILABLE = False
        print(help)
        sleep(2)
        return let_player_guess_letter(file, player)
    # If player has already bought the tip
    elif guess == "tip" and not TIPAVAILABLE and player.health > 1:
        help = fetch_tip(file)
        print("""{Fore.YELLOW} Here the tip again
              {help}""")
        sleep(2)
        return let_player_guess_letter(file, player)
    if guess == "quit":
        quit()

    if len(guess) > 1:
        print(Fore.RED + "You can guess only one letter")
        sleep(2)
        return let_player_guess_letter(file, player)
    else:
        return guess


def print_welcome_message():
    """Print Welcome Message"""
    # Seperated from tutorial message to call tutorial on different places of the game
    print(Fore.CYAN + "\nWelcome to Hangman!\n")


def print_tutorial():
    """Write a tutorial to display at the start of the game"""

    print("""{Fore.YELLOW} How to play:
        {Fore.GREEN} A secret word is chosen. Each underscore represents one secret letter.
        {Fore.GREEN} Guess one letter at a time. If the letter is in the word, its position(s) will be reveal.
        {Fore.GREEN} If the letter is incorrect, you lose one of your guess chances.
        {Fore.GREEN} If you need help, write 'help' to get a tip.
        {Fore.GREEN} Win: All letters are revealed.
        {Fore.RED} Lose: When you have no guesses left.""")


def fetch_player_name(player):
    """Let the user name himself for a more immersiv experience"""
    name = input(Fore.CYAN + "Enter your Name (at least one letter) to start the game or 'q' to end programm: ").capitalize()
    if not name.isalpha():
        print(Fore.RED + "Please enter only letters and no whitespace.\n")
        return fetch_player_name(player)
    elif name == "Q":
        print(f"{Fore.CYAN} Goodbye. Thank you for playing {player.name}")
        quit()
    else:
        return name


def fetch_custom_difficulty(tip_available):
    """Let the user decide how many guesses he wants to have"""
    print("""Fore.CYAN + "You can choose a custom difficulty. The harder you
          want the game to be, the less trys you will have.
        {Fore.GREEN} Easy = 12 wrong guesses
        {Fore.YELLOW} Medium = 8 wrong guesses
        {Fore.MAGENTA} Hard = 4 wrong guesses
        {Fore.RED} Impossible = One wrong guess and you lose""")

    global TIPAVAILABLE

    difficulty_options = [
        inquirer.List(
            'difficulty',
            message=Fore.CYAN + "Choose your difficulty",
            choices=
                [Fore.GREEN + "Easy",
                Fore.YELLOW + "Medium",
                Fore.MAGENTA + "Hard",
                Fore.RED + "Impossible",
                Fore.CYAN + "Leave Game"],
            ),
    ]
    chosen_difficulty = inquirer.prompt(difficulty_options)

    if chosen_difficulty["difficulty"] == Fore.GREEN + "Easy":
        return 12
    elif chosen_difficulty["difficulty"] == Fore.YELLOW + "Medium":
        return 8
    elif chosen_difficulty["difficulty"] == Fore.MAGENTA + "Hard":
        return 4
    elif chosen_difficulty["difficulty"] == Fore.RED + "Impossible":
        TIPAVAILABLE = False
        return 1
    elif chosen_difficulty["difficulty"] == Fore.CYAN + "Leave Game":
        print(Fore.CYAN + "Goodbye")
        quit()


def create_player(player_name, player_difficulty):
    """Create new Player instance"""
    global PLAYEREXISTS
    new_player = Player(player_name, player_difficulty)
    PLAYEREXISTS = True
    return new_player


def display_letter_count(word, guessed_correct_letters):
    """Display the amount of letters the word has as underlines"""
    combined_letters = []
    if len(guessed_correct_letters) == 0:
        print(Fore.CYAN + "The Word is: " +
              Fore.GREEN + " ".join(["_" for letter in word]))
    else:  # Merge guessed Letters and missing letters
        for letter in word:
            if letter in guessed_correct_letters:
                combined_letters.append(letter)
            else:
                combined_letters.append("_")
        print(Fore.CYAN + "The Word is: " +
              Fore.GREEN + " ".join(combined_letters))


def display_already_guessed_letters(wrong_letters):
    """Display the already guessed Letters after each guess"""
    if wrong_letters:
        wrong_letter_list = ", ".join(wrong_letters)
        print(Fore.CYAN + "You already guessed: " + Fore.RED + f"{wrong_letter_list}")


def check_for_already_guessed_letter(guess, correct_guesses, incorrect_guesses, file, player):
    """Check the guess of the user and remind him of already guessed letters"""
    if guess in correct_guesses or guess in incorrect_guesses:
        print(Fore.YELLOW + "You already guessed that letter. Try again")
        return let_player_guess_letter(file, player)
    else:
        return guess


def check_if_anwser_is_correct(guess, word):
    """Check if the guessed letter can be found within the word"""
    safe_validation = []
    for letter in word:
        if guess == letter:
            safe_validation.append(1)
        else:
            pass
    # If no letter was correct it returns an empty list wich is == to False
    return safe_validation


def reduce_player_health(letter_validation, player):
    """Reduces Player health depending on right or wrong guess"""
    if letter_validation:
        return

    player.health -= 1


def append_letter_into_list(letter_validation, guess):
    """Append letter into the specified list"""
    if letter_validation:
        guessed_correct_letters.append(guess)
    else:
        guessed_incorrect_letters.append(guess)


def display_guess_confirmation(guess_letter_validation, player):
    """Display to the User if his guess was correct or incorrect"""
    if guess_letter_validation:
        print(Fore.GREEN + "You guessed correct!")
    else:
        if player.health > 1:
            print(Fore.RED + f"Incorrect. You have {player.health} tries left")
        else:
            return


def ask_for_another_round():
    """Ask the player if he wants to play another round"""
    menu_options = [
        inquirer.List('menu',
                      message="Do you want to play again",
                      choices=["Play again", "Leave Game"],
                      ),
    ]
    chosen_menu = inquirer.prompt(menu_options)
    return chosen_menu["menu"]


def check_for_game_end(player, word, correct_guesses):
    """Checks if the player did win or lose yet"""
    if player.health < 1 or set(correct_guesses) == set(word):
        return True


def end_game(choice):
    if choice == "Play again":
        main()
    else:
        print(Fore.CYAN + "\nGoodbye")
        quit()


def display_game_over(player, word):
    """Display an individual message depending in the loss or win of the player"""
    if player.health == 0:
        print(Fore.RED + f"You lost! The word would have been '{word}'.")
    else:
        print(Fore.GREEN + f"You won and you still had {player.health} tries left. Good job")
        print(Fore.GREEN + f"The word was '{word}'!")


def reset_global_variables():
    """Reset global Variables such as guessed Letters and so on"""
    global guessed_correct_letters
    global guessed_incorrect_letters
    global random_instance

    guessed_correct_letters = []
    guessed_incorrect_letters = []
    random_instance = random.randint(0, 150)


def reset_player_health(difficulty, player):
    """Reset Difficulty / player health after a round"""
    player.health = difficulty


def main():
    global player
    reset_global_variables()
    sleep(1)
    #  Skip function if User already registered Name
    if PLAYEREXISTS:
        pass
    else:
        print_welcome_message()
        print_tutorial()
        player_name = fetch_player_name(player)
    language = let_player_choose_language()
    file_path = fetch_language_file_path(language)
    file = fetch_file(file_path)
    playerHealth = fetch_custom_difficulty()
    #  Skip function if User already exists
    if not PLAYEREXISTS:
        player = create_player(player_name, playerHealth)
    else:
        reset_player_health(playerHealth, player)
    word = fetch_word(file)
    while True:
        sleep(1)
        display_letter_count(word, guessed_correct_letters)
        if guessed_incorrect_letters:
            display_already_guessed_letters(guessed_incorrect_letters)
        sleep(1)
        guess = let_player_guess_letter(file, player)
        check_for_already_guessed_letter(guess, guessed_correct_letters, guessed_incorrect_letters, file, player)
        letter_validation = check_if_anwser_is_correct(guess, word)
        reduce_player_health(letter_validation, player)
        display_guess_confirmation(letter_validation, player)
        append_letter_into_list(letter_validation, guess)
        gameEndValidation = check_for_game_end(player, word, guessed_correct_letters)
        if gameEndValidation:
            display_game_over(player, word)
            userChoice = ask_for_another_round()
            end_game(userChoice)


main()
