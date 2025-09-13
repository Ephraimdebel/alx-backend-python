#!/usr/bin/env python3
import sqlite3
import functools

# -------------- Decorator ----------------
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check if 'query' is passed as a keyword or positional argument
        query = kwargs.get("query")
        if query is None and len(args) > 0:
            query = args[0]
        
        print(f"[LOG] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

# -------------- Function ----------------
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# -------------- Example Run ----------------
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
