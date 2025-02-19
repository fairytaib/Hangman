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
#  Initialize player
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
    if language == Fore.YELLOW + "German":
        file_path = "assets/json/de-words.json"
        print(Fore.CYAN + "\nDu hast Deutsch gewählt.\n")
        return file_path
    elif language == Fore.YELLOW + "Dutch":
        file_path = "assets/json/du-words.json"
        print(Fore.CYAN + "\nJe hebt Nederlands gekozen.\n")
        return file_path
    else:
        file_path = "assets/json/en-words.json"
        print(Fore.CYAN + "\nYou chose english.\n")
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
        print(Fore.CYAN + "\nGoodbye. Thank you for playing\n")
        quit()
    elif chosen_language['language'] == Fore.YELLOW + "Display Rules again":
        print_tutorial()
        sleep(1)
        return let_player_choose_language()

    return chosen_language["language"]


def let_player_guess_letter(file, player):
    """Let the player enter a guessed letter"""
    global TIPAVAILABLE
    if player.health > 1 and TIPAVAILABLE:
        print(Fore.CYAN + "\nGuess one letter. Type 'tip' to buy a tip for "
              "one of your health points or write 'quit' to exit the game.\n")
    elif not TIPAVAILABLE and player.health > 1:
        print(Fore.CYAN + "\nGuess one letter. Type 'tip' to review the"
              "tip or write 'quit' to exit the game.\n")
    else:
        print(Fore.CYAN + "\nGuess one letter."
              " Write 'quit' to exit the game\n")

    guess = input(Fore.CYAN + "\nYour guess: ").lower()

    if guess == "":
        print(Fore.RED + "\nPlease enter at least one letter\n")
        return let_player_guess_letter()
    elif not guess.isalpha():
        print(Fore.RED + "\nOnly letters are allowed\n")
        sleep(1)
        return let_player_guess_letter(file, player)

    if guess == "tip" and TIPAVAILABLE:
        help = fetch_tip(file)
        player.health -= 1
        print(f"""{Fore.YELLOW}You bought a tip.
{Fore.YELLOW}You have now {player.health} tries left.
Here the tip: {help}
""")
        TIPAVAILABLE = False
        sleep(1)
        return let_player_guess_letter(file, player)
    # If player has already bought the tip
    elif guess == "tip" and not TIPAVAILABLE and player.health > 1:
        help = fetch_tip(file)
        print(f"""{Fore.YELLOW} Here the tip again: {help}""")
        sleep(1)
        return let_player_guess_letter(file, player)
    if guess == "quit":
        quit()

    if len(guess) > 1:
        print(Fore.RED + "You can guess only one letter")
        sleep(1)
        return let_player_guess_letter(file, player)
    else:
        return guess


def print_welcome_message():
    """Print Welcome Message"""
    # Seperated from tutorial message to call tutorial on different
    # places of the game
    print(Fore.CYAN + "\nWelcome to Hangman!\n")


def print_tutorial():
    """Write a tutorial to display at the start of the game"""

    print(f"""{Fore.YELLOW}How to play:
{Fore.GREEN}A secret word is chosen. Each underscore represents one
 secret letter.
{Fore.GREEN}Guess one letter at a time. If the letter is in the word,
its position(s) will be reveal.
{Fore.GREEN}If the letter is incorrect, you lose one of your guess chances.
{Fore.GREEN}If you need help, write 'help' to get a tip.
{Fore.GREEN}Win: All letters are revealed.
{Fore.RED}Lose: When you have no guesses left.
""")


def fetch_player_name():
    """Let the user name himself for a more immersiv experience"""
    name = input(f"""{Fore.CYAN}Enter your Name (at least one letter) to
start the game or 'q' to end programm: """).capitalize()

    if name == "":
        print(Fore.RED + "\nPlease enter at least one letter\n")
        return fetch_player_name()
    elif not name.isalpha():
        print(Fore.RED + "\nPlease enter only letters and no whitespace.\n")
        return fetch_player_name()
    elif name == "Q":
        print(f"{Fore.CYAN}\nGoodbye. Thank you for playing\n")
        quit()
    else:
        return name


def display_difficulty_explanation():
    """Display the explanation for the difficulty"""
    print(f"""{Fore.CYAN}You can choose a custom difficulty. The harder you
want the game to be, the less trys you will have.
{Fore.GREEN}Easy = 12 wrong guesses
{Fore.YELLOW}Medium = 8 wrong guesses
{Fore.MAGENTA}Hard = 4 wrong guesses
{Fore.RED}Impossible = One wrong guess and you lose
""")


def fetch_custom_difficulty():
    """Let the user decide how many guesses he wants to have"""

    global TIPAVAILABLE

    print(Fore.CYAN + "\nDifficulty selection:\n")

    difficulty_options = [
        inquirer.List(
                    'difficulty',
                    message=Fore.CYAN + "Choose your difficulty",
                    choices=[
                        Fore.GREEN + "Easy",
                        Fore.YELLOW + "Medium",
                        Fore.MAGENTA + "Hard",
                        Fore.RED + "Impossible",
                        Fore.CYAN + "Leave Game"]
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
        print("""{Fore.CYAN}\nGoodbye.
Thank you very much for playing\n""")
        quit()


def create_player(player_name, player_difficulty):
    """Create new Player instance"""
    global player
    new_player = Player(player_name, player_difficulty)
    player = True
    return new_player


def display_letter_count(word, guessed_correct_letters):
    """Display the amount of letters the word has as underlines"""
    combined_letters = []
    if len(guessed_correct_letters) == 0:
        print(
            f"{Fore.CYAN}The Word is: {Fore.GREEN}"
            f'{" ".join(["_" for letter in word])}'
        )
    else:
        for letter in word:
            if letter in guessed_correct_letters:
                combined_letters.append(letter)
            else:
                combined_letters.append("_")
        print(
            f"{Fore.CYAN}The Word is: {Fore.GREEN}"
            f'{" ".join(combined_letters)}'
        )


def display_already_guessed_letters(wrong_letters):
    """Display the already guessed Letters after each guess"""
    if wrong_letters:
        wrong_letter_list = ", ".join(wrong_letters)
        print(f"{Fore.CYAN}You already guessed: {Fore.RED}{wrong_letter_list}")


def check_for_already_guessed_letter(
      guess, correct_guesses, incorrect_guesses
      ):
    """Check the guess of the user and remind him of already guessed letters"""
    if guess in correct_guesses or guess in incorrect_guesses:
        print(Fore.YELLOW + "\nYou already guessed that letter. Try again.\n")
        return None
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
        print(Fore.GREEN + "\nYou guessed correct!\n")
    else:
        if player.health > 1:
            print(Fore.RED +
                  f"\nIncorrect. You have {player.health} tries left.\n")
        else:
            return


def ask_for_another_round():
    """Ask the player if he wants to play another round"""
    menu_options = [
        inquirer.List(
                    'menu',
                    message=Fore.CYAN + "Do you want to play again",
                    choices=[
                        Fore.CYAN + "Play again",
                        Fore.CYAN + "Leave Game"]
        ),
    ]
    chosen_menu = inquirer.prompt(menu_options)
    return chosen_menu["menu"]


def check_for_game_end(player, word, correct_guesses):
    """Checks if the player did win or lose yet"""
    if player.health < 1 or set(correct_guesses) == set(word):
        return True


def end_game(choice, player):
    if choice == Fore.CYAN + "Play again":
        main()
    else:
        print(Fore.CYAN + f"\nGoodbye. Thank you for playing {player.name}\n")
        quit()


def display_game_over(player, word):
    """Display an individual message
    depending in the loss or win of the player"""
    if player.health == 0:
        print(Fore.RED +
              f"\nYou lost! The word would have been '{word.capitalize()}'.\n")
    else:
        print(f"""
{Fore.GREEN}You won and you still had {player.health} tries left.
 Good job!{Fore.GREEN}The word was '{word.capitaliz()}'!
""")


def reset_global_variables():
    """Reset global Variables such as guessed Letters and so on"""
    global correct_list
    global incorrect_list
    global random_instance

    correct_list = []
    incorrect_list = []
    random_instance = random.randint(0, 150)


def reset_player_health(difficulty, player):
    """Reset Difficulty / player health after a round"""
    player.health = difficulty


def main():
    global player
    global guessed_correct_letters
    global guessed_incorrect_letters
    global 
    reset_global_variables()
    #  Skip function if User already registered Name
    if player:
        pass
    else:
        print_welcome_message()
        print_tutorial()
        sleep(1)
        player_name = fetch_player_name()
    print(Fore.CYAN + "\nLanguage selection:\n")
    language = let_player_choose_language()
    file_path = fetch_language_file_path(language)
    file = fetch_file(file_path)
    display_difficulty_explanation()
    sleep(1)
    playerHealth = fetch_custom_difficulty()
    #  Skip function if User already exists
    if not player:
        player = create_player(player_name, playerHealth)
    else:
        reset_player_health(playerHealth, player)
    word = fetch_word(file)
    while True:
        sleep(1)
        display_letter_count(word, guessed_correct_letters)
        if guessed_incorrect_letters:
            display_already_guessed_letters(guessed_incorrect_letters)
        guess = let_player_guess_letter(file, player)
        guess = check_for_already_guessed_letter(
            guess, guessed_correct_letters,
            guessed_incorrect_letters)
        if guess == None:
            continue
        letter_validation = check_if_anwser_is_correct(guess, word)
        reduce_player_health(letter_validation, player)
        display_guess_confirmation(letter_validation, player)
        append_letter_into_list(letter_validation, guess)
        gameEndValidation = check_for_game_end(
            player, word, guessed_correct_letters)
        sleep(1)
        if gameEndValidation:
            display_game_over(player, word)
            userChoice = ask_for_another_round()
            end_game(userChoice, player)


if __name__ == "__main__":
    main()
