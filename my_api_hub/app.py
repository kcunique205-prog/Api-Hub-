import os
from flask import Flask, render_template_string, request, jsonify, session

# --- CONFIGURATION ---
SECRET_KEY = os.environ.get("SECRET_KEY", "a_very_strong_secret_key_for_apihub_12345")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "ElderChk_Bot") # Aapka bot username

# --- FLASK APP INITIALIZATION ---
app = Flask(__name__)
app.secret_key = SECRET_KEY

# --- HTML TEMPLATES (Ab yeh file alag se nahi chahiye) ---
# Main website ka HTML (index.html)
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Api Hub - Welcome</title>
    <script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>
    <style>
        /* Yahan poora CSS code hai jo pichle message mein tha */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        :root{--primary-color:#8A2BE2;--success-color:#2ecc71;--danger-color:#e74c3c;--shadow-color:rgba(138, 43, 226, 0.4);--border-radius-lg:20px;--border-radius-md:12px;--transition-speed:0.3s;}
        body{font-family:'Inter',sans-serif;background-color:#0d1117;color:#c9d1d9;display:flex;flex-direction:column;justify-content:center;align-items:center;height:100vh;text-align:center;}
        h1{font-size:3rem;}
    </style>
</head>
<body>
    <h1>🔮 Welcome to ApiHub! 🔮</h1>
    <p>Your access is verified. Enjoy the free APIs and source codes.</p>
    <script>feather.replace();</script>
</body>
</html>
"""

# Access code maangne wala page (access_page.html)
ACCESS_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Access Required - ApiHub</title>
    <script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        :root{--primary-color:#8A2BE2; --bg-color:#0d1117; --card-bg:rgba(22, 27, 34, 0.8); --text-color:#c9d1d9; --light-text-color:#8b949e; --border-color:rgba(255, 255, 255, 0.15); --danger-color:#e74c3c;}
        body{font-family:'Inter',sans-serif; background-color:var(--bg-color); color:var(--text-color); display:flex; justify-content:center; align-items:center; height:100vh; margin:0; padding: 20px;}
        .access-container{background:var(--card-bg); padding:40px; border-radius:20px; text-align:center; border:1px solid var(--border-color); max-width:450px; width:100%; backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);}
        h1{margin-bottom:15px; font-size: 1.8rem;} p{color:var(--light-text-color); margin-bottom:30px;}
        input{width:100%; padding:15px; background:rgba(0,0,0,0.2); border:1px solid var(--border-color); border-radius:12px; color:var(--text-color); font-size:1.5rem; text-align:center; letter-spacing: 5px; margin-bottom:20px;}
        .btn{padding:14px 22px; border-radius:12px; border:none; font-weight:600; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:10px; font-size:1rem; width:100%; text-decoration: none; transition: all 0.3s ease;}
        .btn-primary{background:var(--primary-color); color:white; margin-top:20px;} .btn-telegram{background-color:#2AABEE; color:white;}
        .btn:hover{transform: translateY(-3px); box-shadow: 0 4px 15px rgba(0,0,0,0.2);}
        #error-msg{color:var(--danger-color); margin-top:15px; display:none; min-height: 20px;}
    </style>
</head>
<body>
    <div class="access-container">
        <h1>Access Code Required</h1>
        <p>To continue, please get a one-time access code from our Telegram bot.</p>
        <a href="https://t.me/{{ bot_username }}" target="_blank" class="btn btn-telegram" style="margin-bottom: 30px;"><i data-feather="send"></i> Get Access Code Here</a>
        <form id="verify-form">
            <input type="text" id="code-input" placeholder="_ _ _ _ _ _" maxlength="6" required autocomplete="off">
            <button type="submit" class="btn btn-primary">Verify & Enter</button>
        </form>
        <p id="error-msg"></p>
    </div>
    <script>
        document.getElementById('verify-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const code = document.getElementById('code-input').value;
            const errorMsg = document.getElementById('error-msg');
            const submitBtn = e.target.querySelector('button');
            submitBtn.disabled = true; submitBtn.textContent = 'Verifying...'; errorMsg.style.display = 'none';
            try {
                const response = await fetch('/verify', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: `code=${code}` });
                const result = await response.json();
                if (result.success) {
                    submitBtn.textContent = 'Success! Redirecting...'; window.location.reload();
                } else {
                    errorMsg.textContent = result.message || "Verification failed."; errorMsg.style.display = 'block';
                    submitBtn.disabled = false; submitBtn.textContent = 'Verify & Enter';
                }
            } catch (err) {
                errorMsg.textContent = "An error occurred. Please try again."; errorMsg.style.display = 'block';
                submitBtn.disabled = false; submitBtn.textContent = 'Verify & Enter';
            }
        });
        feather.replace();
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    if session.get('authenticated'):
        return render_template_string(INDEX_HTML)
    return render_template_string(ACCESS_PAGE_HTML, bot_username=BOT_USERNAME)

@app.route("/verify", methods=["POST"])
def verify_code():
    # Yeh route ab Redis se communicate karega
    import redis
    r = redis.from_url(os.environ.get("REDIS_URL"))
    
    user_code = request.form.get("code")
    
    # Redis mein code check karein
    user_id = r.get(f"code:{user_code}")
    
    if user_id:
        session['authenticated'] = True
        r.delete(f"code:{user_code}") # Code ko use karne ke baad delete kar dein
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Invalid or expired code."})

