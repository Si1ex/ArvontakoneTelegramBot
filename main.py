from telebot import TeleBot
import random
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')
bot = TeleBot(API_KEY)
players = []
bot.remove_webhook()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Terve! Anna pelaajien nimet pilkulla erotettuna:")
    bot.register_next_step_handler(message, get_players)

def get_players(message):
    global players
    player_names = message.text.strip().split(',')
    players = [name.strip() for name in player_names if name.strip()]
    if players:
        bot.send_message(message.chat.id, f"{len(players)} pelaajaa tallennettu. Valitse kuinka monta pelaajaa valitaan komennolla /pick X, jossa X on pelaajien määrä.")
    else:
        bot.send_message(message.chat.id, "Et antanut pelaajien nimiä. Yritä uudelleen.")
        bot.register_next_step_handler(message, get_players)

@bot.message_handler(commands=['pick'])
def pick_players(message):
    global players
    try:
        count = int(message.text.split()[1])
        if count > 0 and count <= len(players):
            selected_players = random.sample(players, count)
            bot.send_message(message.chat.id, f"Satunnaisesti valitut {count} pelaajaa ovat:\n" + "\n" + "\n".join(selected_players))
        else:
            bot.send_message(message.chat.id, "Virheellinen määrä pelaajia. Yritä uudelleen.")
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Virheellinen syöte. Yritä uudelleen.")

bot.polling(none_stop=True)
