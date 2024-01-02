# Arvontakone

## Description
This Python script is an implementation of a simple drawing or lottery bot using the TeleBot library for Telegram, designed to randomly select a specified number of players from a given list of names.

## Prerequisites
Make sure you have the following prerequisites before running the script:
- Python 3.x installed on your machine
- TeleBot library (`python-telegram-bot`) installed. You can install it using `pip install python-telegram-bot`
- `python-dotenv` library installed. You can install it using `pip install python-dotenv`

## Setup
1. Clone the repository or download the script.
2. Create a new Telegram bot and obtain the API key.
3. Create a `.env` file in the same directory as the script and add the following line:
   ```plaintext
   API_KEY=your_telegram_bot_api_key

Replace your_telegram_bot_api_key with the actual API key you obtained.

##Usage

Run the script using python script_name.py in the terminal.
Start a conversation with the Telegram bot you created.
Use the /start command to initiate the process and enter the names of the players separated by commas when prompted.
After entering the player names, use the /pick X command to randomly select X players from the list.

##Commands
/start: Initiates the bot and prompts the user to enter player names.
/pick X: Randomly selects X players from the entered list of names.
Example
User: /start
Bot: "Hello! Enter the names of the players separated by commas."

User: "John, Jane, Bob, Alice"
Bot: "4 players saved. Choose how many players to pick with the command /pick X, where X is the number of players."

User: /pick 2
Bot: "Randomly selected 2 players are:\nAlice\nJohn"

##Notes

The script handles errors such as invalid input or insufficient players gracefully.
Ensure that the bot has the necessary permissions to read and send messages in the chat.
The script utilizes the python-dotenv library to load the API key from the .env file for security reasons.
Feel free to customize and modify the script according to your needs!
