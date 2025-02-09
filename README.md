# Hangman

![Title Image](./readme-images/start-view.png)

## Descripttion
**Hangman** is a classic word-guessing game where one player thinks of a word, and the other tries to guess it by suggesting letters. The word is represented by a series of blank spaces, with each space corresponding to a letter. If the guessing player suggests a correct letter, it is revealed in its correct position(s). If they guess incorrectly, a part of a stick figure is drawn on a gallows. The game continues until the word is fully guessed or the drawing of the hangman is completed, resulting in a loss. Hangman is often played as a fun and educational game to improve vocabulary and spelling skills.

## Live Version

Experience the game firsthand: [Play Hangman here!](https://hangman-pp3-13b044889c95.herokuapp.com)

![Hangman Start view](./readme-images/start-view.png)

![Hangman language selection](./readme-images/language-selection.png)

![Hangman difficulty selection](./readme-images/difficulty-selection.png)

![Hangman guess letter section](./readme-images/guess-letter-section.png)

![Hangman invalid input](./readme-images/invalid-input.png)

[Hangman correct guess](./readme-images/correct-guess-section.png)

![Hangman incorrect guess](./readme-images/incorrect-guess-section.png)

![Hangman double guessed letter](./readme-images/double-guessed-letter.png)

![Hangman replay section](./readme-images/replay-section.png)

## Features

### Core Gameplay Mechanics

- **Word Selection**:
  - A random word is chosen from a JSON file, supporting multiple languages (English, German, Dutch).
  - Each word comes with a hint that can be purchased using a health point.

- **Turn-Based Letter Guessing**:
  - Players guess one letter at a time.
    ![Hangman guess letter section](./readme-images/guess-letter-section.png)

  - Correct guesses reveal the letter in the word.
    [Hangman correct guess](./readme-images/correct-guess-section.png)

  - Incorrect guesses decrease the player's health.
    ![Hangman incorrect guess](./readme-images/incorrect-guess-section.png)

- **Difficulty Levels**:
  - Players can choose between four difficulty levels:
    - **Easy**: 12 wrong guesses allowed.
    - **Medium**: 8 wrong guesses allowed.
    - **Hard**: 4 wrong guesses allowed.
    - **Impossible**: Only one mistake is allowed.
  - In the **Impossible** mode, hints are disabled for an extreme challenge.
    ![Hangman difficulty selection](./readme-images/difficulty-selection.png)

- **Hint System**:
  - Players can buy a hint in exchange for one health point.
  - If already purchased, the hint can be reviewed anytime.

- **Letter Tracking**:
  - Correctly and incorrectly guessed letters are stored and displayed to help players avoid duplicate guesses.
    ![Hangman double guessed letter](./readme-images/double-guessed-letter.png)

### User Interface and Experience

- **Dynamic Feedback**:
  - Messages and prompts guide the player through the game.
  - Color-coded responses indicate correct (green) and incorrect (red) guesses.

- **Multilingual Support**:
  - The game allows players to choose from different language-based word sets.
    ![Hangman language selection](./readme-images/language-selection.png)

- **Player Customization**:
  - Players enter their name for a personalized experience.
    ![Hangman Start view](./readme-images/start-view.png)

  - Health points vary based on the selected difficulty.
    ![Hangman difficulty selection](./readme-images/difficulty-selection.png)

- **Replayability**:
  - After a game ends (win or lose), players can choose to restart with a new word.
    ![Hangman replay section](./readme-images/replay-section.png)

## Workprocess

### Planning & Design
The development of the Hangman game started with conceptual planning. Using Mimo, a rough flowchart was created to outline the game's structure. The **Player** class was designed with essential attributes such as:
- `self.name` – Stores the player's name.
- `self.health` – Represents the remaining attempts.
- `guessLetter()` – A method for handling letter guesses.

### Word Selection & APIs
To dynamically fetch words, different APIs were considered and tested. The following sources were explored:
- [Dictionary API](https://dictionaryapi.dev)
- [Free Dictionary API](https://publicapi.dev/free-dictionary-api)
- [Random Word API](https://random-word-api.vercel.app)
- [API Ninjas - Random Word](https://www.api-ninjas.com/api/randomword)
- [Random Words GitHub Repository](https://github.com/mcnaveen/Random-Words-API)

However, the API that was supposed to generate a random word along with its description encountered internal issues (HTTP 500 status). Additionally, integrating **Random Word APIs** with **Dictionary APIs** proved problematic, as some generated words were not found in the dictionary.  

### Custom Word List
Due to these limitations, I decided to create my own curated word list instead. This ensured better control over word selection and guaranteed that each word had a corresponding definition.

### Refactoring the Guess Function
Initially, the `guessLetter()` function was a method within the **Player** class. However, to improve self-referencing and maintain cleaner code, the function was refactored and moved outside of the class.

### Implementation
With the structure in place, coding began by implementing the **Player** class and integrating the word-fetching mechanisms. Further steps involved developing game logic, input validation, and user feedback.

### Testing & Refinement
The game underwent multiple testing phases to ensure smooth gameplay and accurate word validation. Adjustments were made to improve user experience, error handling, and overall performance.

## Technologies Used

- **Languages**:
  - Python
  - Json

- **Version Control**:
  - Git: Used for version control to track changes and manage the development process.
  - GitHub: Used as a cloud-based platform to store and share the code repository.
  - GitHub Pages: Used to deploy the game as a static web application for testing, showcasing, and easy access.
  - Gitpod: Used as an integrated development environment (IDE) to write and edit the code.

- **Other Technology**
  - Miro: Used for planning and visualizing game structure, creating flowcharts, and collaborating on gameplay mechanics.
  - Balsamiq Wireframe: Used to create low-fidelity wireframes for UI layout and structure before design implementation.

## Technologies Used

- **Languages**:
  - Python: The core language used to develop the Hangman game, handling game logic, word selection, and user interactions.

- **Version Control**:
  - Git: Used for version control to track changes and manage the development process.
  - GitHub: Used as a cloud-based platform to store and share the code repository.

- **Development Tools**:
  - VS Code: Used as the primary code editor for writing and debugging Python scripts.
  - Git Bash: Used for executing Git commands and managing version control.

- **Deployment**:
  - Heroku: Used to deploy the Hangman game as a web application, making it accessible online.

- **Data Handling**:
  - JSON: Used to store and manage word lists, ensuring flexibility and easy modifications.

- **Planning & Design**:
  - Miro: Used for organizing ideas, structuring the development workflow, and tracking API testing results.

## Getting started

### Prerequisites

To run Hangman locally, ensure you have:

Python 3.x installed on your machine.
The colorama, inquirer, and json libraries installed. You can install them using pip:

```
pip install colorama inquirer
```

### Installation

- Clone the repository:

```
git clone https://github.com/your-username/hangman.git
```

- Navigate to the project folder:
```
cd hangman
```

- Open the hangman.py file in your preferred text editor or IDE.

### How to Play

- Run the game by executing the hangman.py file:
```
python run.py
```

- Follow the on-screen instructions to:
    - Enter your name.
    - Choose a language for the words.
    - Select a difficulty level.
    - Guess letters to uncover the hidden word.

Feel free to modify the code or assets to your liking and explore the different features of the game!



