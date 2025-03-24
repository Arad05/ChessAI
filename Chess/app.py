from flask import Flask, render_template, request, redirect, url_for, jsonify, session, current_app
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
from datetime import datetime, timedelta
from db import close_db, get_db
import psycopg2.extras
import random, string

# Create Flask instance
app = Flask(__name__, template_folder="ChessAI_GUI/templates", static_folder="ChessAI_GUI/static")
print(os.path.join(os.getcwd(), "ChessAI_GUI/static"))


# Set secret key
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(24)
app.config.from_pyfile('config.py')



# Initialize CSRF protection
csrf = CSRFProtect(app)


def create_app():
    app = Flask(__name__)
    # configure app: app.config[...] ...
    
    app.teardown_appcontext(close_db)
    return app


# Fake users database for demo purposes with multiple users
users_db = {
    "orikopilov2007@gmail.com": {
         "password": generate_password_hash("Orik2007"),
         "nickname": "Orik",
         "first_name": "Ori",
         "last_name": "Kopilov",
         "phone_number": "053-225-7111",
         "country": "Israel",
         "rating": 1213,
         "games_history": [
              {"opponent": "Arad Or", "opponent_nickname": "AradO", "result": "win", "date": "2025-03-12 15:30"},
              {"opponent": "John Doe", "opponent_nickname": "JohnD", "result": "draw", "date": "2025-03-11 20:15"}
         ],
         "friends": ["AradO", "JohnD"],
         "role": "admin",
         "ban_end": None
    },
    "arador2007@gmail.com": {
         "password": generate_password_hash("Password123"),
         "nickname": "AradO",
         "first_name": "Arad",
         "last_name": "Or",
         "phone_number": "053-431-0507",
         "country": "Israel",
         "rating": 1185,
        "games_history": [
            {"opponent": "Ori Kopilov", "opponent_nickname": "Orik", "result": "loss", "date": "2025-03-12 15:30"},
         ],
         "friends": ["Orik"],
         "role": "member",
         "ban_end": None
    },
    "johndoe@example.com": {
         "password": generate_password_hash("DoePass456"),
         "nickname": "JohnD",
         "first_name": "John",
         "last_name": "Doe",
         "phone_number": "000-000-0000",
         "country": "USA",
         "rating": 1202,
        "games_history": [
            {"opponent": "Ori Kopilov", "opponent_nickname": "Orik", "result": "draw", "date": "2025-03-11 20:15"},
         ],
         "friends": ["Orik"],
         "role": "user",
         "ban_end": None
    }
}


#
@app.context_processor
def inject_current_user():
    current_user = None
    if 'user' in session:
        # Look up the user in the fake DB
        current_user = users_db.get(session['user'])
    return dict(current_user=current_user)


# Utility function to sanitize input
def sanitize(input_value):
    if isinstance(input_value, str):
        return bleach.clean(input_value)
    return input_value


#Home page
@app.route('/')
def home():
    return render_template('home.html')


#Sign up page
@app.route('/sign_up', methods=['GET', 'POST'])
@csrf.exempt
def sign_up():
    if 'user' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = sanitize(data.get('email'))
            password = data.get('password')  # No hashing, using as provided
            first_name = sanitize(data.get('first_name'))
            last_name = sanitize(data.get('last_name'))
            nickname = sanitize(data.get('nickname'))
            phone_number = sanitize(data.get('phone_number'))
            country = sanitize(data.get('country'))
            
            db = get_db()
            cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Check if email exists
            cur.execute("SELECT email FROM users WHERE email = %s", (email,))
            if cur.fetchone():
                return jsonify({"success": False, "message": "האימייל כבר קיים במערכת."})
            
            # Check that the nickname is unique
            cur.execute("SELECT nickname FROM users WHERE nickname = %s", (nickname,))
            if cur.fetchone():
                return jsonify({"success": False, "message": "הניקניימ כבר בשימוש."})
            
            # Insert the password directly without hashing.
            cur.execute("""
                INSERT INTO users (
                    email, password, first_name, last_name, nickname, 
                    phone_number, country, rating, role
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (email, password, first_name, last_name, nickname, phone_number, country, 1200, 'user'))
            db.commit()
            
            # Create session to log the user in immediately
            session['user'] = email
            session['role'] = 'user'
            
            return jsonify({"success": True, "message": "המשתמש נרשם ונכנס בהצלחה!"})
        except Exception as e:
            current_app.logger.error(f"Error in sign up: {e}")
            return jsonify({"success": False, "message": "שגיאה בשרת"}), 500
    
    return render_template('sign_up.html')


#About page
@app.route('/about')
def about():
    return render_template('about.html')


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        email = session['user']
        db = get_db()
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        print(f"User from session: {user}")

        if user and user["ban_end"] and user["ban_end"] > datetime.now():
            return jsonify({"success": False, "message": "You are banned until " + user["ban_end"].strftime('%Y-%m-%d %H:%M:%S')})
        return redirect(url_for('home'))

    if request.method == 'POST':
        # Remove accidental whitespace from the inputs.
        email = sanitize(request.form.get('email')).strip()
        password = request.form.get('password').strip()

        # Debug prints
        print(f"Email entered: {email!r}")
        print(f"Password entered: {password!r}")

        db = get_db()
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        print(f"User from DB: {user}")
        if user:
            print(f"Stored password: {user['password']}")

        # Compare passwords directly (ONLY FOR TESTING, NOT SECURE)
        if user and user['password'] == password:
            print(f"User authenticated: {user}")
            if user["ban_end"] and user["ban_end"] > datetime.now():
                return jsonify({"success": False, "message": "You are banned until " + user["ban_end"].strftime('%Y-%m-%d %H:%M:%S')})

            session['user'] = email
            session['role'] = user['role']
            return jsonify({"success": True, "message": "Login successful!"})
        else:
            print("Authentication failed: Incorrect email or password.")
            return jsonify({"success": False, "message": "Incorrect email or password"})

    return render_template('login.html')


#Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


#Forgot password page
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    token = sanitize(request.args.get('token')) or sanitize(request.form.get('token'))
    
    if request.method == 'POST':
        db = get_db()
        cur = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if token:
            new_password = request.form.get('new_password')
            if token != session.get('reset_token'):
                return jsonify({"success": False, "message": "Invalid or expired token."})
            email = session.get('user')
            cur.execute("SELECT email FROM users WHERE email = %s", (email,))
            if cur.fetchone():
                # Directly update the password without hashing.
                cur.execute("UPDATE users SET password = %s WHERE email = %s", (new_password, email))
                db.commit()
                session.pop('reset_token', None)
                return jsonify({"success": True, "message": "הסיסמה שונתה בהצלחה!"})
            else:
                return jsonify({"success": False, "message": "משתמש לא קיים."})
        else:
            email = sanitize(request.form.get('email'))
            cur.execute("SELECT email FROM users WHERE email = %s", (email,))
            if cur.fetchone():
                reset_token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
                session['reset_token'] = reset_token
                send_reset_email(email, reset_token)
                return jsonify({"success": True, "message": "קישור לשחזור סיסמה נשלח אליך!"})
            else:
                return jsonify({"success": False, "message": "האימייל לא נמצא במערכת."})
    
    return render_template('forgot_password.html', token=token)


#Reset password function
def send_reset_email(user_email, reset_token):

    sender_email = "orikopilov2007@gmail.com"  # Your email here
    sender_password = "Orik2007"  # Your email password or an app-specific password
    
    receiver_email = user_email
    subject = "שחזור סיסמה - ChessAI"
    body = (f"שלום, \n\nקיבלת קישור לשחזור סיסמה:\n"
            f"http://localhost:5000/reset_password/{reset_token}\n\n"
            "בברכה, צוות ChessAI")

    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"Password reset email sent to {user_email}")
    except Exception as e:
        print(f"Error sending email: {e}")


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

    # Create a User object (assuming your User class accepts these parameters)
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
    
    # Use JSON columns directly (they're already lists/arrays)
    user.games_history = user_info.get("games_history", [])
    user.friends = user_info.get("friends", [])
    
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
@app.route('/update_user_settings', methods=['POST'])
def update_user_settings():
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


# View a friend's profile
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

    # Compute game stats from the JSON column 'games_history'
    games = friend_info.get('games_history', [])
    stats = {
        'wins': sum(1 for game in games if game.get('result') == 'win'),
        'draws': sum(1 for game in games if game.get('result') == 'draw'),
        'losses': sum(1 for game in games if game.get('result') == 'loss')
    }
    
    # Use the JSON column 'friends' directly and convert each friend string into a dict.
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
        'history': games,  # Directly using the games_history JSON data
        'friends': friends_list,  # Now a list of dicts, each with a "nickname" key
        'role': friend_info.get('role', 'user')
    }
    
    return render_template("friend_profile.html", user=friend_data)



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


# New route to record a game result.
@app.route('/record_game', methods=['POST'])
def record_game():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    # Sanitize the opponent nickname and result inputs
    opponent_nickname = sanitize(data.get('opponent_nickname'))
    result = sanitize(data.get('result'))  # Expected: "win", "loss", or "draw"
    if result not in ['win', 'loss', 'draw']:
        return jsonify({'success': False, 'error': 'Invalid result'}), 400

    email = session.get('user')
    if not email or email not in users_db:
        return jsonify({'success': False, 'error': 'User not found'}), 400

    # Instantiate the current user as a User object.
    current_user_data = users_db[email]
    current_user_obj = User(
        email=email,
        password=current_user_data['password'],
        first_name=current_user_data['first_name'],
        last_name=current_user_data['last_name'],
        phone_number=current_user_data['phone_number'],
        country=current_user_data['country'],
        nickname=current_user_data['nickname']
    )

    current_user_obj.rating = current_user_data.get("rating", 1200)
    current_user_obj.games_history = current_user_data.get("games_history", [])

    # Find the opponent by nickname.
    opponent_email = None
    opponent_data = None
    
    for e, info in users_db.items():
        if info.get("nickname") == opponent_nickname:
            opponent_email = e
            opponent_data = info
            break

    if not opponent_data:
        return jsonify({'success': False, 'error': 'Opponent not found'}), 404

    opponent_obj = User(
        email=opponent_email,
        password=opponent_data['password'],
        first_name=opponent_data['first_name'],
        last_name=opponent_data['last_name'],
        phone_number=opponent_data['phone_number'],
        country=opponent_data['country'],
        nickname=opponent_data['nickname']
    )

    opponent_obj.rating = opponent_data.get("rating", 1200)
    opponent_obj.games_history = opponent_data.get("games_history", [])

    # Record the game using the User method.
    current_user_obj.record_game(opponent_obj, result)

    # Update the fake DB with the new ratings and game histories.
    users_db[email]['rating'] = current_user_obj.rating
    users_db[email]['games_history'] = current_user_obj.games_history

    users_db[opponent_email]['rating'] = opponent_obj.rating
    users_db[opponent_email]['games_history'] = opponent_obj.games_history

    return jsonify({'success': True, 'message': 'Game recorded and ratings updated!'}), 200


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
        # Query all users from the actual DB
        cur.execute("SELECT email, nickname, role FROM users")
        all_users = cur.fetchall()
        return render_template("admin_dashboard.html", users=all_users)
    
    if request.method == "POST":
        action = request.form.get("action")
        target_email = sanitize(request.form.get("target_email"))
        message = ""
        
        if action == "promote":
            cur.execute("UPDATE users SET role = 'member' WHERE email = %s AND role = 'user'", (target_email,))
            message = "Promoted successfully" if cur.rowcount else "Promotion failed"
        
        elif action == "demote":
            cur.execute("UPDATE users SET role = 'user' WHERE email = %s AND role = 'member'", (target_email,))
            message = "Demoted successfully" if cur.rowcount else "Demotion failed"

        elif action == "ban":
            try:
                duration = int(request.form.get("duration"))
            except ValueError:
                duration = 0

            if duration > 0:
                cur.execute("UPDATE users SET ban_end = (NOW() + interval '%s minutes') WHERE email = %s", (duration, target_email))
                message = "User banned" if cur.rowcount else "Ban failed"
            else:
                message = "Invalid duration"

        elif action == "unban":
            cur.execute("UPDATE users SET ban_end = NULL WHERE email = %s", (target_email,))
            message = "User unbanned" if cur.rowcount else "Unban failed"

        elif action == "delete":
            # Get the nickname of the user to be deleted
            cur.execute("SELECT nickname FROM users WHERE email = %s", (target_email,))
            user = cur.fetchone()

            if user:
                deleted_nickname = user["nickname"]

                # Remove the user from all friends lists
                cur.execute("""
                    UPDATE users
                    SET friends = friends - %s
                    WHERE friends ? %s
                """, (deleted_nickname, deleted_nickname))

                # Delete the user
                cur.execute("DELETE FROM users WHERE email = %s", (target_email,))
                
                message = "User deleted" if cur.rowcount else "Delete failed"
            else:
                message = "User not found"

        else:
            message = "Unknown action"
        
        db.commit()
        return jsonify({"success": True, "message": message})




if __name__ == "__main__":
    port = 5001 if app.debug else 5003
    app.run(debug=True, port=port)