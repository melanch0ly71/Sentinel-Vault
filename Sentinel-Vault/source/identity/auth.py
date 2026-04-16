import bcrypt
import sqlite3
import logging
from datetime import datetime

# Setup basic logging for the "Forensics" requirement
logging.basicConfig(filename='logs/access_log.txt', level=logging.INFO)

class AuthManager:
    def __init__(self, db_path="identity.db"):
        self.db_path = db_path

    def register_user(self, username, password):
        """Hashes the password and saves the user."""
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode(), salt)
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                             (username, hashed))
            return True
        except sqlite3.IntegrityError:
            return False # User already exists

    def verify_user(self, username, password):
        """Checks credentials and logs the attempt (Audit Trail)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()

        if row and bcrypt.checkpw(password.encode(), row[0]):
            logging.info(f"[{datetime.now()}] SUCCESS: User '{username}' authenticated.")
            return True
        else:
            logging.warning(f"[{datetime.now()}] FAILURE: Unauthorized access attempt for user '{username}'.")
            return False