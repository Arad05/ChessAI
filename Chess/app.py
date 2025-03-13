from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
import smtplib
from flask_wtf.csrf import CSRFProtect
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import string
import random
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


# Create Flask instance
app = Flask(__name__, template_folder="ChessAI_GUI/templates", static_folder="ChessAI_GUI/static")
print(os.path.join(os.getcwd(), "ChessAI_GUI/static"))

# Set secret key
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(24)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Temporary details (delete when DB is complete)
VALID_EMAIL = "orikopilov2007@gmail.com"
VALID_PASSWORD = "Orik2007"

# Fake users database for demo purposes
users_db = {
    "orikopilov2007@gmail.com": {"password": VALID_PASSWORD, "username": "Ori"}
}


@app.route('/')
def home():
    return render_template('home.html')


# Exempt the JSON-based sign-up route from CSRF protection
@csrf.exempt
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = request.get_json()
            print(data)
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            # phone_number and country are not used in this demo logic
            # but you can add validation as needed.

            # Check if email already exists in the fake database
            if email in users_db:
                return jsonify({"success": False, "message": "האימייל כבר קיים במערכת."})

            # Hash password before storing
            hashed_password = generate_password_hash(password)

            # Add the user to the fake database
            users_db[email] = {
                "password": hashed_password,
                "username": first_name + " " + last_name
            }

            return jsonify({"success": True, "message": "המשתמש נרשם בהצלחה!"})
        except Exception as e:
            print(f"Error in sign up: {e}")
            return jsonify({"success": False, "message": "שגיאה בשרת"}), 500
    
    return render_template('sign_up.html')



@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email in users_db:
            # Use check_password_hash instead of direct comparison
            if check_password_hash(users_db[email]['password'], password):
                session['user'] = email
                return jsonify({"success": True})
            else:
                return jsonify({"success": False, "message": "אימייל או סיסמה שגויים"})
        else:
            return jsonify({"success": False, "message": "המשתמש לא קיים"})

    return render_template('login.html')



@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return f"ברוך הבא, {session['user']}!"



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))



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



@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    # Check if a token is provided as a query parameter or via form data.
    token = request.args.get('token') or request.form.get('token')

    if request.method == 'POST':
        # If a token is present, treat this POST as a password reset.
        if token:
            new_password = request.form.get('new_password')
            if token != session.get('reset_token'):
                return jsonify({"success": False, "message": "Invalid or expired token."})
            # Here, determine the email for which the token was generated.
            # For this example, we assume it's stored in session.
            email = session.get('user')
            if email in users_db:
                users_db[email]['password'] = generate_password_hash(new_password)
                session.pop('reset_token', None)  # Optionally clear the token
                return jsonify({"success": True, "message": "הסיסמה שונתה בהצלחה!"})
            else:
                return jsonify({"success": False, "message": "משתמש לא קיים."})
        else:
            # Otherwise, treat it as a request to send a reset email.
            email = request.form.get('email')
            if email in users_db:
                reset_token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
                session['reset_token'] = reset_token
                send_reset_email(email, reset_token)
                return jsonify({"success": True, "message": "קישור לשחזור סיסמה נשלח אליך!"})
            else:
                return jsonify({"success": False, "message": "האימייל לא נמצא במערכת."})
    
    # GET request: render the template. If a token is in the URL, the template will show the reset form.
    return render_template('forgot_password.html', token=token)



@app.route('/play_online')
def play_online():
    return render_template('play_online.html')



@app.route('/play_bot')
def play_bot():
    return render_template('play_bot.html')



if __name__ == "__main__":
    app.run(debug=True, port=5000)
