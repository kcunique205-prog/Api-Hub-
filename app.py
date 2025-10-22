import os
import random
import string
import threading
import time
from flask import Flask, render_template, request, jsonify, session
import telebot

# --- CONFIGURATION (Aapke dwara di gayi details) ---
# Yeh secrets aapko Render ke "Environment Variables" mein set karne honge
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8279866700:AAEZ_-0B4NDHlnrhrj81a6knakqdlCWRRlg")
ADMIN_TELEGRAM_ID = os.environ.get("ADMIN_TELEGRAM_ID", "7126849112")
SECRET_KEY = os.environ.get("SECRET_KEY", "a_very_strong_secret_key_for_apihub") # Ise Render par badal sakte hain

# --- FLASK APP INITIALIZATION ---
app = Flask(__name__)
app.secret_key = SECRET_KEY

# --- TELEGRAM BOT INITIALIZATION ---
bot = telebot.TeleBot(BOT_TOKEN)

# --- IN-MEMORY STORAGE (For simplicity on Render) ---
access_codes = {}  # Stores {user_id: {'code': '123456', 'timestamp': ...}}
user_sessions = {} # Stores {session_id: user_id}
site_visits = 0

# --- TELEGRAM BOT LOGIC ---
@bot.message_handler(commands=['start', 'getcode'])
def send_welcome(message):
    """
    User ko ek naya access code generate karke bhejta hai.
    """
    user_id = message.chat.id
    code = ''.join(random.choices(string.digits, k=6))
    
    # Code ko 5 minute ke liye valid rakhein
    access_codes[user_id] = {'code': code, 'timestamp': time.time()}
    
    bot.reply_to(message, 
        f"👋 Hello!\n\n"
        f"Your one-time access code for ApiHub is:\n\n"
        f"➡️ `{code}` ⬅️\n\n"
        f"This code is valid for 5 minutes. Please enter it on the website.",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['stats'])
def send_stats(message):
    """
    Admin ko website ke statistics bhejta hai.
    """
    if str(message.chat.id) == str(ADMIN_TELEGRAM_ID):
        active_sessions = len(user_sessions)
        bot.reply_to(message, 
            f"📊 *ApiHub Statistics*\n\n"
            f"- *Total Site Visits:* {site_visits}\n"
            f"- *Currently Active Users:* {active_sessions}",
            parse_mode="Markdown"
        )
    else:
        bot.reply_to(message, "Sorry, you are not authorized to use this command.")

# --- FLASK WEB ROUTES ---
@app.route("/")
def home():
    """
    Main page. Check karta hai ki user authenticated hai ya nahi.
    """
    global site_visits
    site_visits += 1
    
    if 'user_id' in session and session.get('authenticated'):
        # Agar authenticated hai, to main website (index.html) dikhayein
        return render_template("index.html")
    
    # Agar nahi, to access code wala page (access_page.html) dikhayein
    bot_username = "ElderChk_Bot" # Aapka bot username
    return render_template("access_page.html", bot_username=bot_username)

@app.route("/verify", methods=["POST"])
def verify_code():
    """
    User dwara submit kiye gaye access code ko verify karta hai.
    """
    user_code = request.form.get("code")
    
    user_id_found = None
    for uid, data in list(access_codes.items()):
        # Check karein ki code match hota hai aur expire nahi hua hai (5 min)
        if data['code'] == user_code and (time.time() - data['timestamp']) < 300:
            user_id_found = uid
            break
            
    if user_id_found:
        # Verification safal
        session['user_id'] = user_id_found
        session['authenticated'] = True # Session ko authenticated mark karein
        user_sessions[session.sid] = user_id_found
        del access_codes[user_id_found] # Code ko ek baar use karne ke baad delete kar dein
        return jsonify({"success": True})
    else:
        # Verification asafal
        return jsonify({"success": False, "message": "Invalid or expired code. Please get a new one from the bot."})

@app.route("/logout")
def logout():
    """
    User ko logout karke session clear karta hai.
    """
    if session.sid in user_sessions:
        del user_sessions[session.sid]
    session.clear()
    return "Logged out"

# --- START THE APP (Render ke liye taiyaar) ---
# Render Gunicorn ka istemal karke is app ko chalayega.
if __name__ == "__main__":
    # Bot ko ek alag thread mein chalayein taaki web server block na ho
    bot_thread = threading.Thread(target=lambda: bot.polling(none_stop=True))
    bot_thread.daemon = True
    bot_thread.start()
    
    # Flask app ko chalayein
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
