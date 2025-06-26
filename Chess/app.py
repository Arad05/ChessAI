import hashlib
import re
from flask import Flask, flash, json, render_template, request, redirect, url_for, jsonify, session, current_app
import os
import smtplib
from flask_wtf.csrf import CSRFProtect
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import string
import random
from werkzeug.security import generate_password_hash, check_password_hash
from user import User
from functools import wraps
import bleach
from user_roles import Member, Admin
from datetime import datetime, time, timedelta, timezone
from db import close_db, get_db
import psycopg2.extras
import random, string
import bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
# Create Flask instance
app = Flask(__name__, template_folder="ChessAI_GUI/templates", static_folder="ChessAI_GUI/static")
print(os.path.join(os.getcwd(), "ChessAI_GUI/static"))

load_dotenv()


# Set secret key
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(24)
app.config.from_pyfile('config.py')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'



limiter = Limiter(get_remote_address, app=app, default_limits=["200 per minute"])


# Initialize CSRF protection
csrf = CSRFProtect(app)


def create_app():
    app = Flask(__name__)
    # configure app: app.config[...] ...
    
    app.teardown_appcontext(close_db)
    return app


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Utility function to sanitize input
def sanitize(input_value):
    if isinstance(input_value, str):
        return bleach.clean(input_value)
    return input_value


#Home page
@app.route('/')
def home():
    return render_template('home.html')


def is_valid_email(email):
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email) and len(email) <= 255

def is_valid_password(password):
    return (
        len(password) >= 8 and len(password) <= 64 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'\d', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    )

def is_valid_phone(phone):
    return re.match(r"^\+?\d{9,15}$", phone)

def is_valid_nickname(nickname):
    return re.match(r"^[a-zA-Z0-9_]{3,20}$", nickname)

# עמוד הרשמה
@app.route('/sign_up', methods=['GET', 'POST'])
@limiter.limit("20 per minute")  # חוסם ניסיונות מרובים תוך דקה
def sign_up():
    if 'user' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = sanitize(data.get('email')).strip()
            password = data.get('password').strip()
            first_name = sanitize(data.get('first_name'))
            last_name = sanitize(data.get('last_name'))
            nickname = sanitize(data.get('nickname'))
            phone_number = sanitize(data.get('phone_number'))
            country = sanitize(data.get('country'))
            
            db = get_db()
            cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # בדיקת קיום אימייל
            cur.execute("SELECT email FROM users WHERE email = %s", (email,))
            if cur.fetchone():
                return jsonify({"success": False, "message": "האימייל כבר קיים במערכת."})

            # בדיקת ייחודיות הניקניימ
            cur.execute("SELECT nickname FROM users WHERE nickname = %s", (nickname,))
            if cur.fetchone():
                return jsonify({"success": False, "message": "הניקניימ כבר בשימוש."})

            # האשינג של הסיסמה
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # שימוש לפני הכנסת הנתונים למסד הנתונים:
            if not is_valid_email(email):
                return jsonify({"success": False, "message": "אימייל לא תקין."})
            if not is_valid_password(password):
                return jsonify({"success": False, "message": "סיסמה לא עומדת בתנאים."})
            if not is_valid_phone(phone_number):
                return jsonify({"success": False, "message": "מספר טלפון לא תקין."})
            if not is_valid_nickname(nickname):
                return jsonify({"success": False, "message": "שם משתמש לא תקין."})
            # הכנסה למסד הנתונים
            cur.execute("""
                INSERT INTO users (
                    email, password, first_name, last_name, nickname, 
                    phone_number, country, rating, role
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (email, hashed_password, first_name, last_name, nickname, phone_number, country, 1200, 'user'))
            db.commit()

            # יצירת סשן והכנסת המשתמש למערכת
            session['user'] = email
            session['role'] = 'user'

            return jsonify({"success": True, "message": "המשתמש נרשם ונכנס בהצלחה!"})

        except Exception as e:
            current_app.logger.error(f"Error in sign up: {e}")
            return jsonify({"success": False, "message": "שגיאה בשרת"}), 500

    return render_template('sign_up.html')

limiter.limit("200 per minute")(sign_up)


#About page
@app.route('/about')
def about():
    return render_template('about.html')


# עמוד התחברות
@limiter.limit("10 per minute")  # חוסם ניסיונות מרובים תוך דקה
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        email = session['user']
        db = get_db()
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        print(f"משתמש מהסשן: {user}")

        if user["ban_end"] and user["ban_end"] > datetime.now(timezone.utc):
            return jsonify({"success": False, "message": f"אתה חסום עד {user['ban_end'].strftime('%Y-%m-%d %H:%M:%S')}"})

    if request.method == 'POST':
        email = sanitize(request.form.get('email')).strip()
        password = request.form.get('password').strip()

        print(f"אמייל שהוזן: {email!r}")
        print(f"סיסמה שהוזנה: {password!r}")

        db = get_db()
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        print(f"משתמש מה-DB: {user}")
        if user:
            stored_hash = user['password']
            
            if isinstance(stored_hash, bytes):
                stored_hash = stored_hash.decode('utf-8')

            print(f"האש מה-DB: {stored_hash!r}")

            if not stored_hash:
                print("שגיאה: ערך ההאש ריק")
                return jsonify({"success": False, "message": "שגיאת התחברות - נסה שנית"})

            # בדיקת מבנה ההאש
            if stored_hash.startswith("$2a$") or stored_hash.startswith("$2b$"):
                print("מזהה האש תקין, בודק התאמה...")
            else:
                print(f"שגיאה: מבנה ההאש לא צפוי: {stored_hash}")
                return jsonify({"success": False, "message": "שגיאת התחברות - נסה שנית"})

            # בדיקת התאמת הסיסמה
            try:
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                    print("התחברות הצליחה!")
                    
                    if user["ban_end"] and user["ban_end"] > datetime.now(timezone.utc):
                        return jsonify({"success": False, "message": f"אתה חסום עד {user['ban_end'].strftime('%Y-%m-%d %H:%M:%S')}"} )
                    
                    user['ban_end'] = None
                    session['user'] = email
                    session['role'] = user['role']
                    session['clan'] = user['clan']
                    session.permanent = True
                    app.permanent_session_lifetime = timedelta(hours=1)  # סשן יפוג אחרי שעה
                    return jsonify({"success": True, "message": "התחברת בהצלחה!"})
                else:
                    print("שגיאה: אימייל או סיסמה שגויים.")
                    return jsonify({"success": False, "message": "אימייל או סיסמה שגויים"})
            except Exception as e:
                print(f"שגיאה בזמן בדיקת הסיסמה: {e}")
                return jsonify({"success": False, "message": "שגיאת מערכת - נסה שנית"})

    return render_template('login.html')

limiter.limit("10 per minute")(login)


#Logout
@app.route('/logout')
def logout():
    session.clear()  # מנקה את כל הנתונים בסשן
    session.modified = True  # מוודא שהשינויים נשמרים
    response = redirect(url_for('login'))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response



#Forgot password page
@limiter.limit("10 per minute")  # מגביל ניסיון שחזור ל-5 לדקה
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    token = sanitize(request.args.get('token')) or sanitize(request.form.get('token'))

    if request.method == 'POST':
        db = get_db()
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        if token:
            new_password = request.form.get('new_password').strip()
            stored_token = session.get('reset_token')
            email = session.get('reset_email')

            if not stored_token or token != stored_token or not email:
                return jsonify({"success": False, "message": "טוקן שגוי או פג תוקף."})

            cur.execute("SELECT password FROM users WHERE email = %s", (email,))
            user = cur.fetchone()

            if not user:
                return jsonify({"success": False, "message": "משתמש לא קיים."})

            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            cur.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
            db.commit()

            session.pop('reset_token', None)
            session.pop('reset_email', None)

            return jsonify({"success": True, "message": "הסיסמה שונתה בהצלחה!"})

        else:
            email = sanitize(request.form.get('email')).strip()
            cur.execute("SELECT email FROM users WHERE email = %s", (email,))
            
            if not cur.fetchone():
                return jsonify({"success": False, "message": "האימייל לא נמצא במערכת."})

            reset_token = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
            session['reset_token'] = reset_token
            session['reset_email'] = email

            send_reset_email(email, reset_token)

            return jsonify({"success": True, "message": "קישור לשחזור סיסמה נשלח אליך!"})

    return render_template('forgot_password.html', token=token)


# not working yet!
def send_reset_email(user_email, reset_token):
    sender_email = os.getenv("BREVO_EMAIL")  
    smtp_username = os.getenv("BREVO_API_KEY")  
    smtp_server = "smtp-relay.brevo.com"
    smtp_port = 587  

    receiver_email = user_email
    subject = "שחזור סיסמה - ChessAI"
    body = f"שלום,\n\nקיבלת קישור לשחזור סיסמה:\nhttp://localhost:5000/forgot_password?token={reset_token}\n\nבברכה, צוות ChessAI"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        print("מתחבר לשרת SMTP...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.set_debuglevel(1)  # Debug SMTP
            server.starttls()  
            print("מבצע התחברות עם שם משתמש (API Key)...")
            server.login(smtp_username, "")  
            print("שולח אימייל ל:", receiver_email)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print(f"אימייל נשלח בהצלחה ל-{user_email}")
    except Exception as e:
        print(f"שגיאה בשליחת אימייל: {e}")




# Updated function to get the current logged-in user based on session data and the fake DB
def get_current_user():
    email = session.get('user')
    if not email:
        return None

    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user_info = cur.fetchone()
    if not user_info:
        return None

    # Create a User object and include clan and clan_role
    user = User(
        email=email,
        password=user_info["password"],
        first_name=user_info.get("first_name", ""),
        last_name=user_info.get("last_name", ""),
        phone_number=user_info.get("phone_number", ""),
        country=user_info.get("country", ""),
        nickname=user_info.get("nickname", "")
    )
    user.rating = user_info.get("rating", 1200)
    user.role = user_info.get("role", "user")
    user.online_status = user_info.get("online_status", False)
    user.games_history = user_info.get("games_history", [])
    user.friends = user_info.get("friends", [])
    
    # New fields:
    user.clan = user_info.get("clan", None)
    user.clan_role = user_info.get("clan_role", None)
    
    return user




# User settings page
@app.route('/user_settings', methods=['GET'])
def user_settings():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    user_data = {
        'nickname': user.nickname,
        'phone': user.phone_number,
        'name': user.first_name,
        'lastName': user.last_name,
        'country': user.country,
        'rating': user.rating,
        'role': user.role,
        'clan': user.clan if user.clan else "None",
        'clan_role': user.clan_role if user.clan_role else "None",
        'stats': {
            'wins': sum(1 for game in user.games_history if game.get('result') == 'win'),
            'draws': sum(1 for game in user.games_history if game.get('result') == 'draw'),
            'losses': sum(1 for game in user.games_history if game.get('result') == 'loss')
        },
        'history': user.games_history,
        'friends': user.friends
    }
    

    return render_template("user_settings.html", user=user_data)


# Update user settings
@csrf.exempt
@app.route('/update_user_settings', methods=['POST'])
def update_user_settings():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        email = session.get('user')
        if not email:
            return jsonify({'success': False, 'error': 'User not found'}), 400

        db = get_db()
        cur = db.cursor()
        phone_number = sanitize(data.get('phone', ''))
        first_name = sanitize(data.get('name', ''))
        last_name = sanitize(data.get('lastName', ''))
        country = sanitize(data.get('country', ''))

        cur.execute("""
            UPDATE users 
            SET phone_number = %s, first_name = %s, last_name = %s, country = %s 
            WHERE email = %s
        """, (phone_number, first_name, last_name, country, email))
        db.commit()

        return jsonify({'success': True, 'message': 'User settings updated successfully!'})
    except Exception as e:
        current_app.logger.error(f"Error updating user settings: {e}")
        return jsonify({'success': False, 'error': 'An error occurred'}), 500



# Friend's profile page
@app.route('/profile/<friend_nickname>')
def profile(friend_nickname):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    friend_nickname = sanitize(friend_nickname)
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Retrieve the friend's info from the users table
    cur.execute("SELECT * FROM users WHERE nickname = %s", (friend_nickname,))
    friend_info = cur.fetchone()
    if not friend_info:
        return "User not found", 404

    games = friend_info.get('games_history', [])
    stats = {
        'wins': sum(1 for game in games if game.get('result') == 'win'),
        'draws': sum(1 for game in games if game.get('result') == 'draw'),
        'losses': sum(1 for game in games if game.get('result') == 'loss')
    }
    
    friends_list = friend_info.get('friends', [])
    if isinstance(friends_list, list) and friends_list and isinstance(friends_list[0], str):
        friends_list = [{'nickname': friend} for friend in friends_list]
    
    friend_data = {
        'nickname': friend_info.get('nickname', ''),
        'name': friend_info.get('first_name', ''),
        'lastName': friend_info.get('last_name', ''),
        'phone': friend_info.get('phone_number', ''),
        'country': friend_info.get('country', ''),
        'rating': friend_info.get('rating', 1200),
        'stats': stats,
        'history': games,
        'friends': friends_list,
        'role': friend_info.get('role', 'user'),
        'clan': friend_info.get('clan', "None"),
        'clan_role': friend_info.get('clan_role', "None")
    }

    # Retrieve all existing nicknames from the database.
    cur.execute("SELECT nickname FROM users")
    users = cur.fetchall()
    existing_users = {user['nickname'] for user in users}
    
    return render_template("friend_profile.html", user=friend_data, existing_users=existing_users)


# Play online page
@app.route('/play_online')
def play_online():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('play_online.html')


# Play offline againts bot page
@app.route('/play_bot')
def play_bot():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('play_bot.html')


# ---------------------------
# New endpoint: Promote a user to member
# ---------------------------
# This endpoint handles two cases:
#   1. Admin-provided: an admin (by username/email) promotes a user.
#   2. Payment-based: a user pays (minimum $5 or equivalent) and is promoted automatically(NOT IMPLEMENTED YET).
# The payment-based promotion is not implemented in this demo.
# Promote to member endpoint (now using the actual DB)
@app.route('/promote_to_member', methods=['POST'])
def promote_to_member():
    data = request.get_json()
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    if "target_email" in data:
        logged_in_user_email = session.get('user')
        if not logged_in_user_email:
            return jsonify({"success": False, "message": "לא מחובר למערכת"}), 403
        
        # Check that the logged-in user is an admin
        cur.execute("SELECT role FROM users WHERE email = %s", (logged_in_user_email,))
        admin_user = cur.fetchone()
        if not admin_user or admin_user.get("role") != "admin":
            return jsonify({"success": False, "message": "הרשאות מנהל דרושות."}), 403
        
        target_email = sanitize(data.get("target_email"))
        cur.execute("SELECT role, nickname FROM users WHERE email = %s", (target_email,))
        target_user = cur.fetchone()
        if not target_user:
            return jsonify({"success": False, "message": "המשתמש לא נמצא."}), 404
        if target_user.get("role") != "user":
            return jsonify({"success": False, "message": "משתמש זה כבר קיים כ-member או admin."}), 400
        
        cur.execute("UPDATE users SET role = 'member' WHERE email = %s", (target_email,))
        db.commit()
        return jsonify({"success": True, "message": f"{target_user.get('nickname')} promoted to member by admin."})
    
    return jsonify({"success": False, "message": "Invalid request data."}), 400


# Admin Dashboard endpoint updated to use the database
@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    current_user = get_current_user()
    if not current_user or current_user.role != "admin":
        return redirect(url_for('login'))
    
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    if request.method == "GET":
        # Query all users including clan info from the actual DB
        cur.execute("SELECT email, nickname, role, clan, clan_role, ban_end FROM users")
        all_users = cur.fetchall()
        
        # Query all clans from the DB
        cur.execute("SELECT * FROM clans")
        all_clans = cur.fetchall()
        
        # Calculate average elo for each clan and add it to the clan dict
        for clan in all_clans:
            clan['average_elo'] = calculate_average_elo(clan["name"])
        
        return render_template("admin_dashboard.html", users=all_users, clans=all_clans)

    
    if request.method == "POST":
        action = request.form.get("action")
        target_email = sanitize(request.form.get("target_email"))
        message = ""
        
        if action == "promote":
            cur.execute("UPDATE users SET role = 'member' WHERE email = %s AND role = 'user'", (target_email,))
            message = "Promoted successfully" if cur.rowcount else "Promotion failed"
            
        elif action == "demote":
            # Fetch user details to check clan membership and nickname
            cur.execute("SELECT clan, nickname FROM users WHERE email = %s AND role = 'member'", (target_email,))
            user_data = cur.fetchone()
            if user_data:
                clan = user_data['clan']
                nickname = user_data['nickname']
                # (1) Remove clan affiliation and (2) Nullify clan_role in users table
                cur.execute(
                    "UPDATE users SET role = 'user', clan = NULL, clan_role = NULL WHERE email = %s",
                    (target_email,)
                )
                # (3) If user belonged to a clan, remove their nickname from the clan's members JSON
                if clan:
                    cur.execute(
                        "UPDATE clans SET members = (members::jsonb - %s)::json WHERE name = %s",
                        (nickname, clan)
                    )
                message = "Demoted successfully"
            else:
                message = "Demotion failed"
    
        elif action == "ban":
            try:
                duration = int(request.form.get("duration"))
            except ValueError:
                duration = 0

            if duration > 0:
                cur.execute("UPDATE users SET ban_end = (NOW() + interval '%s days') WHERE email = %s", (duration, target_email))
                message = "User banned" if cur.rowcount else "Ban failed"
            else:
                message = "Invalid duration"
    
        elif action == "unban":
            # Check if the user is currently banned
            cur.execute("SELECT ban_end FROM users WHERE email = %s", (target_email,))
            user_data = cur.fetchone()
            
            if user_data and user_data["ban_end"] is not None:
                # User is banned, proceed with unbanning
                cur.execute("UPDATE users SET ban_end = NULL WHERE email = %s", (target_email,))
                message = "User unbanned" if cur.rowcount else "Unban failed"
            else:
                message = "User is not banned"

    
        elif action == "delete":
            # Fetch user details to know their clan membership and nickname
            cur.execute("SELECT clan, nickname FROM users WHERE email = %s", (target_email,))
            user_data = cur.fetchone()
            if user_data:
                clan = user_data['clan']
                nickname = user_data['nickname']
                # Remove the user's nickname from any friends lists first
                cur.execute("""
                    UPDATE users
                    SET friends = friends - %s
                    WHERE friends ? %s
                """, (nickname, nickname))
                # (3) Remove the user from the clan's members JSON if they are in a clan
                if clan:
                    cur.execute(
                        "UPDATE clans SET members = (members::jsonb - %s)::json WHERE name = %s",
                        (nickname, clan)
                    )
                # Delete the user record
                cur.execute("DELETE FROM users WHERE email = %s", (target_email,))
                message = "User deleted" if cur.rowcount else "Delete failed"
            else:
                message = "User not found"
    
        else:
            message = "Unknown action"
        
        db.commit()
        return jsonify({"success": True, "message": message})


def get_clan_members(clan_name):
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT members FROM clans WHERE name = %s", (clan_name,))
    row = cur.fetchone()
    cur.close()
    if row and row.get("members"):
        # If the column is stored as JSON in PostgreSQL,
        # psycopg2 may already return a dict. If not, parse it.
        members = row["members"]
        if isinstance(members, str):
            try:
                members = json.loads(members)
            except json.JSONDecodeError:
                members = {}
        return members
    return {}


def calculate_average_elo(clan_name):
    """Calculate the average elo for the clan by looking up each member’s rating."""
    members = get_clan_members(clan_name)
    db = get_db()
    total = 0
    count = 0
    for nickname in members.keys():
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT rating FROM users WHERE nickname = %s", (nickname,))
        user = cur.fetchone()
        cur.close()
        if user and user.get("rating"):
            total += user["rating"]
            count += 1
    return (total / count) if count > 0 else None


def get_clan_member_details(clan_name):
    """
    Retrieve detailed info (nickname, role, rating) for each clan member and 
    return a list sorted by rating in descending order.
    """
    members = get_clan_members(clan_name)
    db = get_db()
    member_details = []
    for nickname, role in members.items():
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT rating FROM users WHERE nickname = %s", (nickname,))
        user = cur.fetchone()
        cur.close()
        rating = user["rating"] if user and user.get("rating") else 0
        member_details.append({"nickname": nickname, "role": role, "rating": rating})
    # Sort the members by rating (highest first)
    member_details.sort(key=lambda m: m["rating"], reverse=True)
    return member_details


@app.route('/clan', methods=['GET', 'POST'])
@login_required
def clan_page():
    if session.get('role') not in ['member', 'admin', 'mod']:
        flash("You must be a member, mod, or admin to access this page.")
        return redirect(url_for('home'))
    
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cur.execute("SELECT * FROM users WHERE email = %s", (session['user'],))
    user_info = cur.fetchone()
    
    clan_info = None
    clan_admin = None
    members_details = []

    if user_info and user_info.get("clan"):
        cur.execute("SELECT * FROM clans WHERE name = %s", (user_info["clan"],))
        clan_info = cur.fetchone()
        
        cur.execute("SELECT nickname FROM users WHERE clan = %s AND clan_role = 'Leader' LIMIT 1", (user_info["clan"],))
        admin_info = cur.fetchone()
        clan_admin = admin_info["nickname"] if admin_info else "N/A"

        avg_elo = calculate_average_elo(clan_info["name"])
        clan_info["average_elo"] = avg_elo
        members_details = get_clan_member_details(clan_info["name"])

    if request.method == "POST" and "clan_name" in request.form:
        search_name = request.form.get("clan_name", "").strip()
        if search_name:
            cur.execute("SELECT * FROM clans WHERE name ILIKE %s", (search_name,))
            clan_info = cur.fetchone()
            if clan_info:
                cur.execute("SELECT nickname FROM users WHERE clan = %s AND clan_role = 'Leader' LIMIT 1", (clan_info["name"],))
                admin_info = cur.fetchone()
                clan_admin = admin_info["nickname"] if admin_info else "N/A"
                
                avg_elo = calculate_average_elo(clan_info["name"])
                clan_info["average_elo"] = avg_elo
                members_details = get_clan_member_details(clan_info["name"])
            else:
                flash("No clan found with that name.")
    
    db.commit()
    cur.close()
    return render_template("clan.html", clan=clan_info, clan_admin=clan_admin, members_details=members_details, current_user=user_info)


@app.route('/clan_action', methods=['POST'])
@login_required
def clan_action():
    """
    Handles promote, demote, and kick actions.
    Expects form data:
      - action: 'promote', 'demote', or 'kick'
      - target: the nickname of the target user
    """
    action = request.form.get("action")
    target = request.form.get("target")
    current_user_email = session.get("user")
    
    db = get_db()
    cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Get current user info and their clan including clan_role.
    cur.execute("SELECT clan, nickname, clan_role FROM users WHERE email = %s", (current_user_email,))
    current_info = cur.fetchone()
    if not current_info or not current_info.get("clan"):
        flash("You are not in a clan.")
        return redirect(url_for('clan_page'))
    
    clan_name = current_info["clan"]
    current_clan_role = current_info.get("clan_role", "member")  # default to member if not set
    
    # Get the target user's info to ensure they are in the same clan.
    cur.execute("SELECT nickname, clan, clan_role FROM users WHERE nickname = %s", (target,))
    target_info = cur.fetchone()
    if not target_info or target_info.get("clan") != clan_name:
        flash("Target user is not in your clan.")
        return redirect(url_for('clan_page'))
    
    # Get the clan's current members dictionary.
    cur.execute("SELECT members FROM clans WHERE name = %s", (clan_name,))
    clan_row = cur.fetchone()
    if clan_row:
        members = clan_row["members"]
        if isinstance(members, str):
            try:
                members = json.loads(members)
            except json.JSONDecodeError:
                members = {}
    else:
        flash("Clan not found.")
        return redirect(url_for('clan_page'))

    # Disallow any changes to the Leader.
    if target_info["clan_role"] == "Leader":
        flash("Cannot modify the leader.")
        return redirect(url_for('clan_page'))
    
    # Process the action.
    if action == "kick":
        if current_clan_role not in ["Leader", "mod"]:
            flash("You are not allowed to kick members.")
            return redirect(url_for('clan_page'))
        # Remove clan association and clan role for the target.
        cur.execute("UPDATE users SET clan = NULL, clan_role = NULL WHERE nickname = %s", (target,))
        if target in members:
            del members[target]
        flash(f"{target} has been kicked from the clan.")
    
    elif action == "promote":
        # Only allow promoting a member.
        if target_info["clan_role"] != "member":
            flash("Only members can be promoted.")
            return redirect(url_for('clan_page'))
        if current_clan_role not in ['Leader', 'mod']:
            flash("You are not allowed to promote members.")
            return redirect(url_for('clan_page'))
        cur.execute("UPDATE users SET clan_role = 'mod' WHERE nickname = %s", (target,))
        members[target] = "mod"
        flash(f"{target} has been promoted to mod.")
    
    elif action == "demote":
        # Only a Leader can demote a mod.
        if target_info["clan_role"] != "mod":
            flash("Only mods can be demoted.")
            return redirect(url_for('clan_page'))
        if current_clan_role != "Leader":
            flash("Only clan leaders can demote mods.")
            return redirect(url_for('clan_page'))
        cur.execute("UPDATE users SET clan_role = 'member' WHERE nickname = %s", (target,))
        members[target] = "member"
        flash(f"{target} has been demoted to member.")
    
    else:
        flash("Invalid action.")
        return redirect(url_for('clan_page'))
    
    # Update the clan's members JSON in the clans table.
    cur.execute("UPDATE clans SET members = %s WHERE name = %s", (json.dumps(members), clan_name))
    db.commit()
    cur.close()
    return redirect(url_for('clan_page'))


@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    try:
        sender = session.get('user')
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({'success': False, 'error': 'Invalid JSON data'}), 400

        receiver = sanitize(data.get('to'))
        message_text = sanitize(data.get('message'))

        if not sender or not receiver or not message_text:
            return jsonify({'success': False, 'error': 'Invalid data'}), 400

        db = get_db()
        cur = db.cursor()

        cur.execute("SELECT conversations FROM messages WHERE nickname = %s", (sender,))
        sender_data = cur.fetchone()
        raw_conversations = sender_data[0] if sender_data else None
        if isinstance(raw_conversations, str):
            conversations = json.loads(raw_conversations)
        elif isinstance(raw_conversations, dict):
            conversations = raw_conversations
        elif raw_conversations is None:
            conversations = {}
        else:
            conversations = {}


        conversations.setdefault(receiver, []).append({
            'from': sender,
            'message': message_text,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        cur.execute("""
            INSERT INTO messages (nickname, conversations)
            VALUES (%s, %s)
            ON CONFLICT (nickname)
            DO UPDATE SET conversations = EXCLUDED.conversations
        """, (sender, json.dumps(conversations)))

        db.commit()
        return jsonify({'success': True, 'message': 'Message sent!'})

    except Exception as e:
        print("Error while sending message:", e)
        return jsonify({'success': False, 'error': 'Server error occurred'}), 500




@app.route('/messages/<friend_nickname>')
@login_required
def show_messages(friend_nickname):
    user = session.get('user')
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT conversations FROM messages WHERE nickname = %s", (user,))
    row = cur.fetchone()
    conversations = row[0] if row else {}

    messages = conversations.get(friend_nickname, [])
    messages.sort(key=lambda m: m['timestamp']) # Sort messages by timestamp

    return render_template('messages.html', friend_nickname=friend_nickname, messages=messages, current_user=session.get('user'))


if __name__ == "__main__":
    port = 5001 if app.debug else 5003
    app.run(debug=True, port=port)