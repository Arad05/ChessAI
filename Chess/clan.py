from typing import Dict, List

from flask import json
from user import User
from db import get_connection

class Clan:
    MAX_MEMBERS = 50

    def __init__(self, name: str, about: str, leader: User, required_elo: int, is_private: bool = False):
        """
        Initialize a new Clan and insert it into the database.
        The leader becomes the clan owner.
        """
        self.name = name
        self.about = about
        self.required_elo = required_elo
        self.is_private = is_private
        self.members: Dict[User, str] = {}  # Maps a User object to their clan role.
        self.chat: List[dict] = []  # Chat history as a list of dicts.
        self.join_requests: List[User] = []  # For private clans.
        
        # Insert clan into the database and get its generated ID.
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO clans (name, about, required_elo, is_private) VALUES (%s, %s, %s, %s) RETURNING id",
            (self.name, self.about, self.required_elo, self.is_private)
        )
        self.id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        # Set up the leader.
        self.members[leader] = "Leader"
        leader.clan = self
        leader.clan_role = "Leader"
        # Update leader's record in the user table.
        self._update_user_clan_in_db(leader, "Leader")
        print(f"Clan '{self.name}' created with leader {leader.nickname}.")

    @property
    def num_players(self) -> int:
        """Return the number of members in the clan."""
        return len(self.members)

    @property
    def average_elo(self) -> float:
        """Compute the average Elo rating of the clan members."""
        if not self.members:
            return 0.0
        total = sum(member.rating for member in self.members)
        return total / len(self.members)

    def can_join(self, user: User) -> bool:
        """Check if a user meets the requirements to join."""
        if self.num_players >= Clan.MAX_MEMBERS:
            print("Clan is full.")
            return False
        if user.rating < self.required_elo:
            print(f"{user.nickname} does not meet the required Elo ({self.required_elo}).")
            return False
        return True

    def join(self, user: User) -> None:
        """
        Add a user to the clan (and update the DB).
        For public clans, the user is added immediately.
        For private clans, a join request is recorded.
        """
        if user.clan is not None:
            print(f"{user.nickname} is already in a clan.")
            return

        if not self.can_join(user):
            return

        if self.is_private:
            if user not in self.join_requests:
                self.join_requests.append(user)
                print(f"{user.nickname} has requested to join the private clan '{self.name}'.")
            else:
                print(f"{user.nickname} already has a pending join request.")
        else:
            self.members[user] = "member"
            user.clan = self
            user.clan_role = "member"
            self._update_user_clan_in_db(user, "member")
            print(f"{user.nickname} has joined the clan '{self.name}' as a member.")

    def _update_user_clan_in_db(self, user: User, clan_role: str) -> None:
        """Helper method to update a user record in the DB with clan info."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE \"user\" SET clan_id = %s, clan_role = %s WHERE email = %s",
            (self.id, clan_role, user.email)
        )
        conn.commit()
        cur.close()
        conn.close()

    # Additional methods (approve_request, remove_member, promote_member, etc.)
    # should similarly update both the in-memory structure and the DB.

    def send_chat_message(self, user: User, message: str) -> None:
        """
        Add a message to the clan chat (and update the DB if desired).
        """
        if user not in self.members:
            print(f"{user.nickname} is not a member of the clan and cannot send messages.")
            return

        self.chat.append({"sender": user.nickname, "message": message})
        print(f"{user.nickname} says: {message}")

        # Optionally, update the clan's chat in the DB.
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE clans SET chat = %s WHERE id = %s",
            (json.dumps(self.chat), self.id)
        )
        conn.commit()
        cur.close()
        conn.close()

    def show_chat(self) -> None:
        """Display the clan chat history."""
        print(f"--- Clan '{self.name}' Chat ---")
        for msg in self.chat:
            print(f"{msg['sender']}: {msg['message']}")

    
