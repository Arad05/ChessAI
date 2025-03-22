"""
This module defines a User class for a chess-related application.
The User class includes attributes for user details, friend management,
game history tracking, rating updates, messaging, and online status management.
"""

from datetime import datetime

class User:
    """
    Represents a user in the chess application.
    Users can send friend requests, record games, send messages, and track their rating.
    """

    used_nicknames = set()  # Class variable to track used nicknames

    def __init__(self, email: str, password: str, first_name: str, last_name: str,
                 phone_number: str, country: str, nickname: str):
        """
        Initializes a new user with personal details and game-related attributes.
        """
        
        # Assign basic user details
        self.email = email
        self.password = password  # In a real program, this should be hashed
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.country = country
        self.nickname = nickname
        User.used_nicknames.add(nickname)

        # Initialize user-related attributes
        self.friends = set()  # A set of other User objects who are friends
        self.games_history = []  # List of dictionaries representing past games
        self.join_date = datetime.now()  # Timestamp of when the user joined
        self.rating = 1200  # Default chess rating using the ELO system
        self.online_status = False  # Online/offline status of the user
        self.chat_box = {}  # Dictionary mapping friend emails to message lists
        self.friend_requests = set()  # Set of pending friend request users

    
    def send_friend_request(self, friend):
        """
        Sends a friend request to another user if they are not already a friend or pending.
        """
        if friend != self and friend not in self.friends and friend not in self.friend_requests:
            friend.friend_requests.add(self)  # Add request to the recipient's pending requests
            print(f"Friend request sent to {friend.first_name}.")
        else:
            print("Cannot send friend request.")

    
    def accept_friend_request(self, friend):
        """
        Accepts a pending friend request and adds the user to the friends list.
        """
        if friend in self.friend_requests:
            self.friends.add(friend)  # Add friend to both users' friend lists
            friend.friends.add(self)
            self.friend_requests.remove(friend)  # Remove request after accepting
            friend.friend_requests.discard(self)
            print(f"{friend.first_name} added as a friend.")
        else:
            print("No friend request from this user.")

    
    def decline_friend_request(self, friend):
        """
        Declines and removes a friend request if it exists.
        """
        if friend in self.friend_requests:
            self.friend_requests.remove(friend)  # Remove request from pending list
            print(f"Friend request from {friend.first_name} declined.")
        else:
            print("No friend request from this user.")

    
    def record_game(self, opponent, result):
        """
        Records the result of a chess game for both players and updates their ratings.
        """
        if result not in {'win', 'loss', 'draw'}:
            print("Invalid game result.")
            return
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Store game details for both players
        game = {
            'opponent': f"{opponent.first_name} {opponent.last_name}",
            'opponent_email': opponent.email,
            'result': result,
            'date': current_time
        }
        self.games_history.append(game)
        
        opponent_result = 'win' if result == 'loss' else 'loss' if result == 'win' else 'draw'
        opponent.games_history.append({
            'opponent': f"{self.first_name} {self.last_name}",
            'opponent_email': self.email,
            'result': opponent_result,
            'date': current_time
        })

        # Update player ratings based on the result
        self.update_rating(opponent, result)
        opponent.update_rating(self, opponent_result)

    
    def update_rating(self, opponent, result):
        """
        Updates the player's ELO rating based on the result of a game.
        """
        k_factor = 32  # Standard K-factor in chess ELO system
        expected_score = 1 / (1 + 10 ** ((opponent.rating - self.rating) / 400))
        actual_score = 1 if result == 'win' else 0 if result == 'loss' else 0.5
        new_rating = self.rating + k_factor * (actual_score - expected_score)
        self.rating = round(new_rating)  # Round to nearest whole number
        print(f"{self.first_name}'s new rating: {self.rating}")

    
    def send_message(self, friend, message):
        """
        Sends a message to a friend and records the conversation.
        """
        if friend in self.friends:
            # Initialize message history if not already set
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
        """
        Updates the user's online status.
        """
        self.online_status = status
        print(f"{self.first_name} is now {'online' if status else 'offline'}.")

    
    def __str__(self):
        """
        Returns a string representation of the user, including name, nickname, rating, and friends count.
        """
        return f"User: {self.first_name} {self.last_name} (Nickname: {self.nickname}), Rating: {self.rating}, Friends: {len(self.friends)}, Games Played: {len(self.games_history)}"
