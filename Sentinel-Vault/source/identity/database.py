import sqlite3

class IdentityDB:
    def __init__(self, db_path="identity.db"):
        self.db_path = db_path
        self.bootstrap()

    def bootstrap(self):
        """Creates the user table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash BLOB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()