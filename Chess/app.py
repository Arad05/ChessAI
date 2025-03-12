from flask import Flask, render_template
import os

app = Flask(__name__, template_folder="ChessAI_GUI/templates", static_folder="ChessAI_GUI/static")
print(os.path.join(os.getcwd(), "ChessAI_GUI/static"))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():

    return render_template('login.html')


@app.route('/sign_Up')
def sign_Up():

    return render_template('sign_Up.html')


@app.route('/about')
def about():

    return render_template('about.html')


@app.route('/play_online')
def play_online():
    # Logic for playing online
    return render_template('play_online.html')

@app.route('/play_bot')
def play_bot():
    # Logic for playing against a bot
    return render_template('play_bot.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
