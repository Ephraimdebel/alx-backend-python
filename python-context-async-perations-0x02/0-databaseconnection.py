#!/usr/bin/env python3
import sqlite3


class DatabaseConnection:
    """Custom context manager for handling SQLite DB connections."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
        # Returning False ensures exceptions are not suppressed
        return False


if __name__ == "__main__":
    # Example usage: fetch all users
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
