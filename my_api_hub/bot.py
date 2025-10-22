import os
import random
import string
import telebot
import redis

# --- CONFIGURATION ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8279866700:AAEZ_-0B4NDHlnrhrj81a6knakqdlCWRRlg")
ADMIN_TELEGRAM_ID = os.environ.get("ADMIN_TELEGRAM_ID", "7126849112")
REDIS_URL = os.environ.get("REDIS_URL")

# --- INITIALIZATION ---
bot = telebot.TeleBot(BOT_TOKEN)
r = redis.from_url(REDIS_URL)

print("Bot is starting...")

@bot.message_handler(commands=['start', 'getcode'])
def send_welcome(message):
    user_id = message.chat.id
    code = ''.join(random.choices(string.digits, k=6))
    
    # Code ko Redis mein save karein, 5 minute (300 seconds) ke liye
    r.set(f"code:{code}", user_id, ex=300)
    
    bot.reply_to(message, 
        f"👋 Hello!\n\n"
        f"Your one-time access code for ApiHub is:\n\n"
        f"➡️ `{code}` ⬅️\n\n"
        f"This code is valid for 5 minutes.",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['stats'])
def send_stats(message):
    if str(message.chat.id) == str(ADMIN_TELEGRAM_ID):
        # Stats abhi simple rakha gaya hai
        bot.reply_to(message, "📊 Stats feature is under development in this new setup.")
    else:
        bot.reply_to(message, "Sorry, you are not authorized.")

# Bot ko hamesha chalu rakhein
bot.infinity_polling()
