from datetime import datetime

class User:
    used_nicknames = set()  # Class variable to track used nicknames

    def __init__(self, email: str, password: str, first_name: str, last_name: str,
                 phone_number: str, country: str, nickname: str):
        
        
        self.email = email
        self.password = password  # In a real program, this should be hashed
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.country = country
        self.nickname = nickname
        User.used_nicknames.add(nickname)
        self.friends = set()  # A set of other User objects
        self.games_history = []  # List of game results
        self.join_date = datetime.now()
        self.rating = 1200  # Default chess rating
        self.online_status = False
        self.chat_box = {}  # Dictionary where keys are friend emails and values are lists of messages
        self.friend_requests = set()  # Pending friend requests

    def send_friend_request(self, friend):
        if friend != self and friend not in self.friends and friend not in self.friend_requests:
            friend.friend_requests.add(self)
            print(f"Friend request sent to {friend.first_name}.")
        else:
            print("Cannot send friend request.")

    def accept_friend_request(self, friend):
        if friend in self.friend_requests:
            self.friends.add(friend)
            friend.friends.add(self)
            self.friend_requests.remove(friend)
            friend.friend_requests.discard(self)
            print(f"{friend.first_name} added as a friend.")
        else:
            print("No friend request from this user.")

    def decline_friend_request(self, friend):
        if friend in self.friend_requests:
            self.friend_requests.remove(friend)
            print(f"Friend request from {friend.first_name} declined.")
        else:
            print("No friend request from this user.")

    def record_game(self, opponent, result):
        """Add game to both players' histories and update ratings."""
        if result not in {'win', 'loss', 'draw'}:
            print("Invalid game result.")
            return
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        game = {
            'opponent': f"{opponent.first_name} {opponent.last_name}",
            'opponent_email': opponent.email,
            'result': result,
            'date': current_time
        }
        self.games_history.append(game)
        # Record the complementary result for the opponent
        opponent_result = 'win' if result == 'loss' else 'loss' if result == 'win' else 'draw'
        opponent.games_history.append({
            'opponent': f"{self.first_name} {self.last_name}",
            'opponent_email': self.email,
            'result': opponent_result,
            'date': current_time
        })

        self.update_rating(opponent, result)
        opponent.update_rating(self, opponent_result)

    def update_rating(self, opponent, result):
        """Calculate new ELO rating based on the game result."""
        k_factor = 32  # Standard K-factor in chess
        expected_score = 1 / (1 + 10 ** ((opponent.rating - self.rating) / 400))
        actual_score = 1 if result == 'win' else 0 if result == 'loss' else 0.5
        new_rating = self.rating + k_factor * (actual_score - expected_score)
        self.rating = round(new_rating)
        print(f"{self.first_name}'s new rating: {self.rating}")

    def send_message(self, friend, message):
        if friend in self.friends:
            if friend.email not in self.chat_box:
                self.chat_box[friend.email] = []
            self.chat_box[friend.email].append((self.first_name, message))
            if self.email not in friend.chat_box:
                friend.chat_box[self.email] = []
            friend.chat_box[self.email].append((self.first_name, message))
            print(f"Message sent to {friend.first_name}.")
        else:
            print("You can only message friends.")

    def set_online_status(self, status: bool):
        self.online_status = status
        print(f"{self.first_name} is now {'online' if status else 'offline'}.")

    def __str__(self):
        return f"User: {self.first_name} {self.last_name} (Nickname: {self.nickname}), Rating: {self.rating}, Friends: {len(self.friends)}, Games Played: {len(self.games_history)}"
