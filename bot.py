import telebot
import os
from flask import Flask, request
import requests

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
CHANNEL_USERNAME = "@downloadvideo77"
subscribed_users = set()

def is_user_subscribed(user_id):
    url = f"https://api.telegram.org/bot{TOKEN}/getChatMember"
    params = {
        "chat_id": CHANNEL_USERNAME,
        "user_id": user_id
    }
    response = requests.get(url, params=params)
    data = response.json()
    try:
        status = data['result']['status']
        return status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if is_user_subscribed(user_id):
        bot.reply_to(message, "🎉 شكراً على الاشتراك في القناة ✅\nيمكنك الآن استخدام البوت بكل سهولة.")
        subscribed_users.add(user_id)
    else:
        bot.reply_to(message, "مرحبًا بكم في أسرع بوت لتحميل الفيديو من أي منصة في برامج التواصل الاجتماعي:\nيوتيوب – تيك توك – فيسبوك – سناب شات وغيرها...\n\n📢 لاستخدام البوت، الرجاء الاشتراك في القناة أولاً:\n👉 https://t.me/downloadvideo77\n\nبعد الاشتراك، أرسل /start من جديد ✅")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id == message.chat.id:
        if not subscribed_users:
            bot.reply_to(message, "⚠️ لا يوجد مشتركين مسجلين بعد.")
            return
        msg = message.text.replace('/broadcast', '').strip()
        if not msg:
            bot.reply_to(message, "✏️ الرجاء كتابة الرسالة بعد الأمر /broadcast")
            return
        count = 0
        for user_id in subscribed_users:
            try:
                bot.send_message(user_id, f"📢 رسالة إدارية:\n{msg}")
                count += 1
            except:
                pass
        bot.reply_to(message, f"✅ تم إرسال الرسالة إلى {count} مشترك.")

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
