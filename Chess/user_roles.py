"""
This module defines extended user classes: Member and Admin.
"""

from user import User
from datetime import datetime
from clan import Clan  # Import the Clan class

class Member(User):
    """
    A Member has all User capabilities plus:
      - The ability to create a clan.
      - The ability to challenge bots (including those tagged as "Members Only").
    """
    def __init__(self, email, password, first_name, last_name, phone_number, country, nickname):
        super().__init__(email, password, first_name, last_name, phone_number, country, nickname)
        self.role = "member"     # Application role flag
        self.clan = None         # The clan the user belongs to
        self.clan_role = None    # Clan-specific role: None, "member", "mod", or "Leader"
    

    def create_clan(self, clan_name: str, required_elo: int, is_private: bool = False):
        """
        Creates a clan for the member.
        The creator becomes the Leader of the clan.
        """
        if self.clan is not None:
            print(f"{self.nickname} is already in a clan.")
            return

        # Create a new Clan instance with self as the leader.
        self.clan = Clan(clan_name, "About " + clan_name, self, required_elo, is_private)
        self.clan_role = "Leader"
        # The Clan.__init__ call already updates the DB.



    def fight_bot(self, bot):
        """
        Allows the member to fight a bot.
        If the bot is tagged "Members Only", only members (or higher) can fight it.
        """
        if bot.get("members_only", False):
            print(f"{self.nickname} is challenging a 'Members Only' bot: {bot.get('name')}.")
        else:
            print(f"{self.nickname} is challenging bot: {bot.get('name')}.")
        # Add additional logic to simulate a fight
        

class Admin(Member):
    """
    An Admin has all Member capabilities plus:
      - A dashboard to view all users.
      - Functions to promote/demote users.
      - Ability to ban or delete users.
    """
    def __init__(self, email, password, first_name, last_name, phone_number, country, nickname):
        super().__init__(email, password, first_name, last_name, phone_number, country, nickname)
        self.role = "admin"
    

    def view_all_users(self, users_db: dict):

        """Returns a list of all users with basic information."""
        return [{ "email": email, "nickname": data.get("nickname"), "role": data.get("role", "user") }
                for email, data in users_db.items()]
    

    def promote_user(self, target_email: str, users_db: dict):

        """Promote a user to member if they are not already a member or admin."""
        if target_email in users_db:
            user = users_db[target_email]
            if user.get("role", "user") == "user":
                user["role"] = "member"
                print(f"User {user.get('nickname')} promoted to member.")
                return True
            else:
                print("User is already a member or admin.")
        return False


    def demote_member(self, target_email: str, users_db: dict):

        """Demote a member to a regular user."""
        if target_email in users_db:
            user = users_db[target_email]
            if user.get("role") == "member":
                user["role"] = "user"
                print(f"Member {user.get('nickname')} demoted to user.")
                return True
            else:
                print("User is not a member.")
        return False


    def ban_user(self, target_email: str, duration_minutes: int, users_db: dict):

        """Bans a user for a certain amount of time. (This is a stub implementation.)"""
        if target_email in users_db:
            users_db[target_email]["banned_until"] = datetime.now().timestamp() + (duration_minutes * 60)
            print(f"User {users_db[target_email].get('nickname')} banned for {duration_minutes} minutes.")
            return True
        return False
    
    
    def unban_user(self, target_email: str, users_db: dict):
        """Unbans a user by removing the ban."""
        if target_email in users_db:
            user = users_db[target_email]
            if "banned_until" in user and user["banned_until"] > datetime.now().timestamp():
                # Unban the user by removing the ban
                del user["banned_until"]
                print(f"User {user.get('nickname')} has been unbanned.")
                return True
            else:
                print("User is not banned or the ban has already expired.")
        else:
            print("User not found.")
        return False

    def delete_user(self, target_email: str, users_db: dict):
        """Deletes a user from the database and removes them from everyone's friend list."""
        if target_email in users_db:
            deleted_user = users_db.pop(target_email)
            deleted_nickname = deleted_user.get("nickname")

            # Remove the deleted user from all friends lists
            for user in users_db.values():
                if "friends" in user and deleted_nickname in user["friends"]:
                    user["friends"].remove(deleted_nickname)

            print(f"User {deleted_nickname} has been deleted and removed from all friend lists.")
            return True
        return False

    
