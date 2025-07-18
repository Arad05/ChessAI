from flask import Flask, render_template
import os

app = Flask(__name__, template_folder="ChessAI_GUI/templates", static_folder="ChessAI_GUI/static")

@app.route('/')
def home():
    return render_template('home.html')

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
