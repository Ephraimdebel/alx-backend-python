#!/usr/bin/env python3
import sqlite3


class ExecuteQuery:
    """Custom context manager to execute a query with parameters."""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.results = None

    def __enter__(self):
        # Open connection
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        # Execute query
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results  # return results to the with-block

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
        return False  # don't suppress exceptions


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    # Using the context manager
    with ExecuteQuery("users.db", query, params) as results:
        print(results)
