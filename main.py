from telebot import TeleBot
import random
from dotenv import load_dotenv
import os

load_dotenv()   #Load environment variables from .env file

API_KEY = os.getenv('API_KEY')
bot = TeleBot(API_KEY)
bot.remove_webhook()

players = []
selected_players = []
count = 0

@bot.message_handler(commands=['start'])    #Welcome message handler
def start(message):
    global players, selected_players, count     #Global variables
    players = []
    selected_players = []
    count = 0
    bot.send_message(message.chat.id, "Terve! Anna pelaajien nimet välilyönnillä erotettuna:")
    bot.register_next_step_handler(message, get_players)    #Register next step handler

def get_players(message):            #Get players handler
    global players
    player_input = message.text.strip()     #Strip message from whitespaces
    if player_input.lower() == "/gg":
        bot.send_message(message.chat.id, "Good game!")
        return
    
    if player_input.lower() == "/start":
        start(message)
    else:
        invalid_commands = ["/reroll", "/delete"]
        if any(command in player_input.lower() for command in invalid_commands):    #Check if message contains invalid commands
            bot.send_message(message.chat.id, "Virheellinen syöte. Yritä uudelleen.")
        else:
            player_names = [name.strip() for name in player_input.split(' ') if name.strip()]   #Split message to list of names
            players = player_names

            if len(players) >= 2:
                bot.send_message(message.chat.id, f"{len(players)} pelaajaa tallennettu. Valitse kuinka monta pelaajaa arvotaan kirjoittamalla komento /pick X, jossa X on pelaajien määrä.")
            else:
                bot.send_message(message.chat.id, "Kirjoita enemmän pelaajien nimiä ja yritä uudelleen.")

@bot.message_handler(commands=['pick'])     #Pick players handler
def pick_players(message):
    global players, selected_players, count
    player_input = message.text.strip()    #Strip message from whitespaces

    invalid_commands = ["/reroll"]

    if any(command in player_input.lower() for command in invalid_commands):    #Check if message contains invalid commands
        bot.send_message(message.chat.id, "Virheellinen syöte. Yritä uudelleen.")
        return

    try:
        count = int(message.text.split()[1])    #Get count from message
        if count > 0 and count <= len(players) and count != len(selected_players):  #Check if count is valid
            selected_players = random.sample(players, count)    #Pick players
            bot.send_message(message.chat.id, f"{count} satunnaisesti valittua pelaajaa on:\n" + "\n" + "\n".join(selected_players) + "\n" + "\n" + "Jos haluat arpoa uudelleen, kirjoita komento /reroll. Jos haluat poistaa pelaajia listasta, kirjoita komento /delete ja pelaajien nimet välilyönnillä erotettuna.")
        else:
            bot.send_message(message.chat.id, "Virheellinen määrä pelaajia tai arvonta on jo suoritettu. Yritä uudelleen.")
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Virheellinen syöte. Yritä uudelleen.")


@bot.message_handler(commands=['gg'])   #Good game -message handler
def good_game(message):
    try:
        bot.send_message(message.chat.id, "Good game!")
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Virheellinen syöte. Yritä uudelleen.")

@bot.message_handler(commands=['reroll'])   #Reroll players draw handler
def reroll_players(message):
    global players, selected_players, count
    if len(players) >= 2 and selected_players:  #Check if players list is not empty
        try:
            if 0 < count <= len(players):   #Check if count is valid
                selected_players = random.sample(players, count)    #Reroll players
                bot.send_message(message.chat.id, f"{count} uudelleen valittua pelaajaa on:\n" + "\n" + "\n".join(selected_players) + "\n" + "\n" + "Jos haluat arpoa uudelleen, kirjoita komento /reroll. Jos haluat poistaa pelaajia listasta, kirjoita komento /delete ja pelaajien nimet välilyönnillä erotettuna.")
            else:
                bot.send_message(message.chat.id, "Virheellinen määrä pelaajia. Yritä uudelleen.")
        except (ValueError, IndexError):
            bot.send_message(message.chat.id, "Virheellinen syöte. Yritä uudelleen.")
    else:
        selected_players = []
        bot.send_message(message.chat.id, "Väärä komento tai arvontaa ei ole vielä suoritettu. Yritä uudelleen.")

@bot.message_handler(commands=['delete'])   #Remove players handler
def remove_players(message):
    global players, selected_players, count
    player_input = message.text.strip()   #Strip message from whitespaces

    player_input_lower = player_input.lower()   #Lowercase message

    if "/delete" in player_input_lower:
        player_input = player_input.replace("/delete", "").strip()

    player_names_to_remove = [name.strip().lower() for name in player_input.split(' ') if name.strip()]  #Split message to list of names
    
    if not player_names_to_remove or len(player_names_to_remove) > len(players):    #Check if list is empty or too long
        bot.send_message(message.chat.id, "Virheellinen syöte. Yritä uudelleen.")
        return

    players = [player for player in players if player.lower() not in player_names_to_remove]    #Remove players from list
    selected_players = []   #Reset selected players

    bot.send_message(message.chat.id, f"Nimet poistettu onnistuneesti. Jäljellä olevat pelaajat: {', '.join(players)}")

    if len(players) < 2:
        bot.send_message(message.chat.id, "Pelaajien määrä on alle kaksi. Anna lisää pelaajien nimiä /start-komennolla.")

bot.polling(none_stop=True)    #Start bot