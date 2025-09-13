#!/usr/bin/env python3
import sqlite3
import functools

def log_queries(func):
    """Decorator to log SQL queries before executing them."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Capture the query argument (can be positional or keyword)
        query = kwargs.get("query")
        if query is None and len(args) > 0:
            query = args[0]

        print(f"Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
