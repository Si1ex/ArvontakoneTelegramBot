from telebot import TeleBot
import random
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')
bot = TeleBot(API_KEY)
bot.remove_webhook()

players = []
selected_players = []
count = 0

@bot.message_handler(commands=['start'])
def start(message):
    global players, selected_players, count
    players = []
    selected_players = []
    count = 0
    bot.send_message(message.chat.id, "Terve! Anna pelaajien nimet välilyönnillä erotettuna:")
    bot.register_next_step_handler(message, get_players)

def get_players(message):
    global players
    player_input = message.text.strip()
    if player_input.lower() == "/gg":
        bot.send_message(message.chat.id, "Good game!")
        return
    
    if player_input.lower() == "/start":
        start(message)
    else:
        invalid_commands = ["/reroll", "/delete"]
        if any(command in player_input.lower() for command in invalid_commands):
            bot.send_message(message.chat.id, "Virheellinen syöte. Yritä uudelleen.")
        else:
            player_names = [name.strip() for name in player_input.split(' ') if name.strip()]
            players = player_names

            if len(players) >= 2:
                bot.send_message(message.chat.id, f"{len(players)} pelaajaa tallennettu. Valitse kuinka monta pelaajaa arvotaan kirjoittamalla komento /pick X, jossa X on pelaajien määrä.")
            else:
                bot.send_message(message.chat.id, "Kirjoita enemmän pelaajien nimiä ja yritä uudelleen.")

@bot.message_handler(commands=['pick'])
def pick_players(message):
    global players, selected_players, count
    player_input = message.text.strip()

    invalid_commands = ["/reroll"]

    if any(command in player_input.lower() for command in invalid_commands):
        bot.send_message(message.chat.id, "Virheellinen syöte. Yritä uudelleen.")
        return

    try:
        count = int(message.text.split()[1])
        if count > 0 and count <= len(players) and count != len(selected_players):
            selected_players = random.sample(players, count)
            bot.send_message(message.chat.id, f"{count} satunnaisesti valittua pelaajaa on:\n" + "\n" + "\n".join(selected_players) + "\n" + "\n" + "Jos haluat arpoa uudelleen, kirjoita komento /reroll. Jos haluat poistaa pelaajia listasta, kirjoita komento /delete ja pelaajien nimet välilyönnillä erotettuna.")
        else:
            bot.send_message(message.chat.id, "Virheellinen määrä pelaajia tai arvonta on jo suoritettu. Yritä uudelleen.")
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Virheellinen syöte. Yritä uudelleen.")


@bot.message_handler(commands=['gg'])
def good_game(message):
    try:
        bot.send_message(message.chat.id, "Good game!")
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Virheellinen syöte. Yritä uudelleen.")

@bot.message_handler(commands=['reroll'])
def reroll_players(message):
    global players, selected_players, count
    if len(players) >= 2 and selected_players:
        try:
            if 0 < count <= len(players):
                selected_players = random.sample(players, count)
                bot.send_message(message.chat.id, f"{count} uudelleen valittua pelaajaa on:\n" + "\n" + "\n".join(selected_players) + "\n" + "\n" + "Jos haluat arpoa uudelleen, kirjoita komento /reroll. Jos haluat poistaa pelaajia listasta, kirjoita komento /delete ja pelaajien nimet välilyönnillä erotettuna.")
            else:
                bot.send_message(message.chat.id, "Virheellinen määrä pelaajia. Yritä uudelleen.")
        except (ValueError, IndexError):
            bot.send_message(message.chat.id, "Virheellinen syöte. Yritä uudelleen.")
    else:
        selected_players = []
        bot.send_message(message.chat.id, "Väärä komento tai arvontaa ei ole vielä suoritettu. Yritä uudelleen.")

@bot.message_handler(commands=['delete'])
def remove_players(message):
    global players, selected_players, count
    player_input = message.text.strip()

    player_input_lower = player_input.lower()

    if "/delete" in player_input_lower:
        player_input = player_input.replace("/delete", "").strip()

    player_names_to_remove = [name.strip().lower() for name in player_input.split(' ') if name.strip()]
    
    if not player_names_to_remove or len(player_names_to_remove) > len(players):
        bot.send_message(message.chat.id, "Virheellinen syöte. Yritä uudelleen.")
        return

    players = [player for player in players if player.lower() not in player_names_to_remove]
    selected_players = []

    bot.send_message(message.chat.id, f"Nimet poistettu onnistuneesti. Jäljellä olevat pelaajat: {', '.join(players)}")

    if len(players) < 2:
        bot.send_message(message.chat.id, "Pelaajien määrä on alle kaksi. Anna lisää pelaajien nimiä /start-komennolla.")

bot.polling(none_stop=True)