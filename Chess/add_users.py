import psycopg2
from werkzeug.security import generate_password_hash
from db import get_db

# Users dictionary
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

def add_users_to_db():
    db = get_db()
    cursor = db.cursor()

    # Add users
    for email, user_data in users_db.items():
        cursor.execute("""
            INSERT INTO users (email, password, nickname, first_name, last_name, phone_number, country, rating, role, ban_end)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            email,
            user_data['password'],
            user_data['nickname'],
            user_data['first_name'],
            user_data['last_name'],
            user_data['phone_number'],
            user_data['country'],
            user_data['rating'],
            user_data['role'],
            user_data['ban_end']
        ))

        # Add games history
        for game in user_data['games_history']:
            cursor.execute("""
                INSERT INTO games (user_email, opponent_email, result, game_date)
                VALUES (%s, %s, %s, %s)
            """, (
                email,
                game['opponent'],
                game['result'],
                game['date']
            ))

        # Add friends
        for friend in user_data['friends']:
            cursor.execute("""
                INSERT INTO user_friends (user_email, friend_email)
                VALUES (%s, %s)
            """, (
                email,
                friend
            ))

    # Commit and close the connection
    db.commit()
    cursor.close()
    print("Users added to the database successfully.")

if __name__ == "__main__":
    add_users_to_db()
