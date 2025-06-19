import telebot
import os
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أهلاً بك! هذا بوت مجاني يعمل 24/7 ✨")

@app.route(f"/{TOKEN}", methods=["POST"])
def receive_update():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/')
def index():
    return "بوت شغال ✅"

if __name__ == "__main__":
    import threading

    def polling():
        bot.infinity_polling()

    thread = threading.Thread(target=polling)
    thread.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
