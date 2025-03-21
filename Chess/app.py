from flask import Flask, render_template, request, redirect, url_for, jsonify, session
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

# Create Flask instance
app = Flask(__name__, template_folder="ChessAI_GUI/templates", static_folder="ChessAI_GUI/static")
print(os.path.join(os.getcwd(), "ChessAI_GUI/static"))


# Set secret key
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(24)



# Initialize CSRF protection
csrf = CSRFProtect(app)



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



# Utility function to sanitize input
def sanitize(input_value):
    if isinstance(input_value, str):
        return bleach.clean(input_value)
    return input_value

@app.context_processor
def inject_current_user():
    current_user = None
    if 'user' in session:
        # Look up the user in the fake DB
        current_user = users_db.get(session['user'])
    return dict(current_user=current_user)


#Home page
@app.route('/')
def home():
    return render_template('home.html')



# Sign - up functionExempt the JSON-based sign-up route from CSRF protection
@csrf.exempt
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if 'user' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        try:
            data = request.get_json()

            # Sanitize all input values
            email = sanitize(data.get('email'))
            password = data.get('password')
            first_name = sanitize(data.get('first_name'))
            last_name = sanitize(data.get('last_name'))
            nickname = sanitize(data.get('nickname'))
            phone_number = sanitize(data.get('phone_number'))
            country = sanitize(data.get('country'))

            # Check if email already exists
            if email in users_db:
                return jsonify({"success": False, "message": "האימייל כבר קיים במערכת."})

            # Check that the nickname is unique
            for user in users_db.values():
                if user.get('nickname') == nickname:
                    return jsonify({"success": False, "message": "הניקניימ כבר בשימוש."})

            # Hash the password before storing
            hashed_password = generate_password_hash(password)

            # Store the new user with the nickname
            users_db[email] = {
                "password": hashed_password,
                "first_name": first_name,
                "last_name": last_name,
                "nickname": nickname,
                "phone_number": phone_number,
                "country": country,
                "games_history": [],
                "friends": [],
                "role": "user"
            }

            return jsonify({"success": True, "message": "המשתמש נרשם בהצלחה!"})
        except Exception as e:
            print(f"Error in sign up: {e}")
            return jsonify({"success": False, "message": "שגיאה בשרת"}), 500

    return render_template('sign_up.html')



#About page
@app.route('/about')
def about():
    return render_template('about.html')



#Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        email = session['user']
        user = users_db.get(email)
        if user and user["ban_end"] and user["ban_end"] > datetime.now():
            return jsonify({"success": False, "message": "You are banned until " + user["ban_end"].strftime('%Y-%m-%d %H:%M:%S')})
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = sanitize(request.form.get('email'))
        password = request.form.get('password')

        if email in users_db:
            user = users_db[email]
            if check_password_hash(user['password'], password):
                if user["ban_end"] and user["ban_end"] > datetime.now():
                    return jsonify({"success": False, "message": "You are banned until " + user["ban_end"].strftime('%Y-%m-%d %H:%M:%S')})
                session['user'] = email
                session['role'] = user['role']
                return jsonify({"success": True})
            else:
                return jsonify({"success": False, "message": "Incorrect email or password"})
        else:
            return jsonify({"success": False, "message": "User does not exist"})

    return render_template('login.html')





#Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))



#Forgot password page
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():


    # Sanitize token input
    token = sanitize(request.args.get('token')) or sanitize(request.form.get('token'))

    if request.method == 'POST':

        # If a token is present, treat this POST as a password reset.
        if token:
            new_password = request.form.get('new_password')
            if token != session.get('reset_token'):
                return jsonify({"success": False, "message": "Invalid or expired token."})
            
            # Use the email stored in session to update the password.
            email = session.get('user')

            if email in users_db:
                users_db[email]['password'] = generate_password_hash(new_password)
                session.pop('reset_token', None)
                return jsonify({"success": True, "message": "הסיסמה שונתה בהצלחה!"})
            else:
                return jsonify({"success": False, "message": "משתמש לא קיים."})
            
        else:

            # Otherwise, treat it as a request to send a reset email.
            email = sanitize(request.form.get('email'))

            if email in users_db:
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
    if not email or email not in users_db:
        return None
    
    user_info = users_db[email]

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
    user.games_history = user_info.get("games_history", [])
    user.role = user_info.get("role", "user")  # Ensure role is included
    
    # Set role from session if necessary
    user.role = session.get('role', user.role)

    # Build a list of friend objects using their nickname. This is a simplified version and assumes that the nickname is unique.
    friends_list = []
    for friend_nickname in user_info.get("friends", []):
        friend_data = next((data for data in users_db.values() if data.get("nickname") == friend_nickname), None)
        if friend_data:
            friends_list.append({
                "nickname": friend_data.get("nickname", ""),
                "name": f"{friend_data.get('first_name', '')} {friend_data.get('last_name', '')}"
            })
    user.friends = friends_list

    return user


# User settings page
@app.route('/user_settings', methods=['GET'])
def user_settings():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    # Pass user data (including the rating) to the front end.
    user_data = {
        'nickname': user.nickname,
        'phone': user.phone_number,
        'name': user.first_name,
        'lastName': user.last_name,
        'country': user.country,
        'rating': user.rating,
        'role': user.role,
        'stats': {
            'wins': sum(1 for game in user.games_history if game['result'] == 'win'),
            'draws': sum(1 for game in user.games_history if game['result'] == 'draw'),
            'losses': sum(1 for game in user.games_history if game['result'] == 'loss')
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
    if not email or email not in users_db:
        return jsonify({'success': False, 'error': 'User not found'}), 400

    # Sanitize input values before updating the DB.
    users_db[email]['phone_number'] = sanitize(data.get('phone', users_db[email].get('phone_number')))
    users_db[email]['first_name'] = sanitize(data.get('name', users_db[email].get('first_name')))
    users_db[email]['last_name'] = sanitize(data.get('lastName', users_db[email].get('last_name')))
    users_db[email]['country'] = sanitize(data.get('country', users_db[email].get('country')))

    return jsonify({'success': True, 'message': 'User settings updated successfully!'})



@app.route('/profile/<friend_nickname>')
def profile(friend_nickname):
    if 'user' not in session:
        return redirect(url_for('login'))

    friend_nickname = sanitize(friend_nickname)
    friend_email = None
    friend_info = None

    for email, info in users_db.items():
        if info.get('nickname') == friend_nickname:
            friend_email = email
            friend_info = info
            break

    if not friend_info:
        return "User not found", 404

    stats = {
        'wins': sum(1 for game in friend_info.get("games_history", []) if game['result'] == 'win'),
        'draws': sum(1 for game in friend_info.get("games_history", []) if game['result'] == 'draw'),
        'losses': sum(1 for game in friend_info.get("games_history", []) if game['result'] == 'loss')
    }

    friend_data = {
        'nickname': friend_info.get('nickname', ''),
        'name': friend_info.get('first_name', ''),
        'lastName': friend_info.get('last_name', ''),
        'phone': friend_info.get('phone_number', ''),
        'country': friend_info.get('country', ''),
        'rating': friend_info.get('rating', 1200),
        'stats': stats,
        'history': friend_info.get("games_history", []),
        'friends': [],
        'role': friend_info.get('role', 'user')
    }

    # Fetch friends data
    friends_list = []

    for f_nickname in friend_info.get("friends", []):
        f_data = next((data for data in users_db.values() if data.get("nickname") == f_nickname), None)
        if f_data:
            friends_list.append({
                "nickname": f_data.get("nickname", ""),
                "name": f"{f_data.get('first_name', '')} {f_data.get('last_name', '')}"
            })
    friend_data['friends'] = friends_list

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
#   2. Payment-based: a user pays (minimum $5 or equivalent) and is promoted automatically.
# The payment-based promotion is not implemented in this demo.
@app.route('/promote_to_member', methods=['POST'])
def promote_to_member():
    data = request.get_json()

    # Case 1: Admin promotion (requires admin_email and target_email)
    if "target_email" in data:
        # Check if the current logged-in user is an admin
        logged_in_user_email = session.get('user')
        if not logged_in_user_email:
            return jsonify({"success": False, "message": "לא מחובר למערכת"}), 403

        admin_user = users_db.get(logged_in_user_email)
        if admin_user is None or admin_user.get("role") != "admin":
            return jsonify({"success": False, "message": "הרשאות מנהל דרושות."}), 403
        
        target_email = sanitize(data.get("target_email"))
        target_user = users_db.get(target_email)
        
        if not target_user:
            return jsonify({"success": False, "message": "המשתמש לא נמצא."}), 404
        if target_user.get("role", "user") != "user":
            return jsonify({"success": False, "message": "משתמש זה כבר קיים כ-member או admin."}), 400
        
        # Promote the target user
        target_user["role"] = "member"
        return jsonify({"success": True, "message": f"{target_user.get('nickname')} promoted to member by admin."})

    # Case 2: Payment-based promotion (not implemented in this demo)
    elif "target_email" in data and "payment_amount" in data and "currency" in data:
        target_email = sanitize(data.get("target_email"))
        payment_amount = float(data.get("payment_amount"))
        currency = data.get("currency").strip().upper()

        # Simple conversion rates relative to USD (for example purposes only)
        conversion_rates = {
            "USD": 1.0,
            "EUR": 1.1,
            "ILS": 0.28
        }
        rate = conversion_rates.get(currency, None)
        if rate is None:
            return jsonify({"success": False, "message": "מטבע לא נתמך."}), 400
        
        # Convert the payment to USD equivalent
        usd_equiv = payment_amount * rate
        if usd_equiv < 5:
            return jsonify({"success": False, "message": "Payment is less than the required amount."}), 400
        
        # Promote the user if they exist and are not already a member/admin
        target_user = users_db.get(target_email)
        if not target_user:
            return jsonify({"success": False, "message": "המשתמש לא נמצא."}), 404
        if target_user.get("role", "user") != "user":
            return jsonify({"success": False, "message": "משתמש זה כבר קיים כ-member או admin."}), 400
        
        target_user["role"] = "member"
        return jsonify({"success": True, "message": f"{target_user.get('nickname')} promoted to member via payment."})

    return jsonify({"success": False, "message": "Invalid request data."}), 400




# ---------------------------
# New endpoint: Admin Dashboard
# ---------------------------
@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    current_user = get_current_user()
    if not current_user or current_user.role != "admin":
        return redirect(url_for('login'))
    
    # For GET, display all users
    if request.method == "GET":
        admin_instance = Admin(
            email=session["user"],
            password="",
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            phone_number=current_user.phone_number,
            country=current_user.country,
            nickname=current_user.nickname
        )
        all_users = admin_instance.view_all_users(users_db)
        return render_template("admin_dashboard.html", users=all_users)
    
    # For POST, process admin actions
    if request.method == "POST":
        action = request.form.get("action")
        target_email = request.form.get("target_email")
        admin_instance = Admin(
            email=session["user"],
            password="",
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            phone_number=current_user.phone_number,
            country=current_user.country,
            nickname=current_user.nickname
        )
        message = ""
        if action == "promote":
            success = admin_instance.promote_user(target_email, users_db)
            message = "Promoted successfully" if success else "Promotion failed"
        elif action == "demote":
            success = admin_instance.demote_member(target_email, users_db)
            message = "Demoted successfully" if success else "Demotion failed"
        elif action == "ban":
            try:
                duration = int(request.form.get("duration"))
            except:
                duration = 0
            success = admin_instance.ban_user(target_email, duration, users_db)
            message = "User banned" if success else "Ban failed"
        elif action == "unban":
            success = admin_instance.unban_user(target_email, users_db)
            message = "User unbanned" if success else "Unban failed"
        elif action == "delete":
            success = admin_instance.delete_user(target_email, users_db)
            message = "User deleted" if success else "Delete failed"
        else:
            message = "Unknown action"
        return jsonify({"success": True, "message": message})

    


if __name__ == "__main__":
    port = 5001 if app.debug else 5003
    app.run(debug=True, port=port)