import os
import random
import threading
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# خادم Flask صغير لإبقاء البوت مستيقظاً
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running 24/7 🚀"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

TOKEN = os.getenv("BOT_TOKEN", "8949827475:AAFAS40cv_Jkr0X2oDcJPZWpkuiTamyNlos")
bot = telebot.TeleBot(TOKEN)
scores = {}

CHOICES = {
    "rock": "🪨 حجرة",
    "paper": "📄 ورقة",
    "scissors": "✂️ مقص"
}

@bot.message_handler(commands=['start', 'play'])
def start_game(message):
    user_id = message.chat.id
    if user_id not in scores:
        scores[user_id] = {"player": 0, "bot": 0}
        
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🪨 حجرة", callback_data="rock"),
        InlineKeyboardButton("📄 ورقة", callback_data="paper"),
        InlineKeyboardButton("✂️ مقص", callback_data="scissors")
    )
    
    bot.send_message(
        user_id, 
        "🎮 **لعبة حجرة - ورقة - مقص**\n\nاختر حركتك بالضغط على أحد الأزرار أدناه:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data in ["rock", "paper", "scissors"])
def play_round(call):
    user_id = call.message.chat.id
    player_choice = call.data
    bot_choice = random.choice(["rock", "paper", "scissors"])
    
    if user_id not in scores:
        scores[user_id] = {"player": 0, "bot": 0}

    if player_choice == bot_choice:
        result = "🤝 **تعادل!**"
    elif (player_choice == "rock" and bot_choice == "scissors") or \
         (player_choice == "paper" and bot_choice == "rock") or \
         (player_choice == "scissors" and bot_choice == "paper"):
        result = "🎉 **أنت الفائز!**"
        scores[user_id]["player"] += 1
    else:
        result = "🤖 **البوت هو الفائز!**"
        scores[user_id]["bot"] += 1

    p_score = scores[user_id]["player"]
    b_score = scores[user_id]["bot"]
    
    text = (
        f"انت اخترت: {CHOICES[player_choice]}\n"
        f"البوت اختار: {CHOICES[bot_choice]}\n\n"
        f"{result}\n\n"
        f"🏆 **النتيجة الحالية:**\n"
        f"👤 أنت: {p_score}  |  🤖 البوت: {b_score}"
    )

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🪨 حجرة", callback_data="rock"),
        InlineKeyboardButton("📄 ورقة", callback_data="paper"),
        InlineKeyboardButton("✂️ مقص", callback_data="scissors")
    )

    bot.edit_message_text(
        chat_id=user_id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=markup,
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    print("البوت يعمل الآن...")
    bot.infinity_polling()
