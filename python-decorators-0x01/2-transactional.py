import sqlite3
import functools


def with_db_connection(func):
    """Decorator to provide a database connection to the function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")  # adjust DB name if needed
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def transactional(func):
    """Decorator to handle transaction management"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # commit if successful
            return result
        except Exception as e:
            conn.rollback()  # rollback on failure
            print(f"Transaction rolled back due to error: {e}")
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )
    print("User email updated successfully")


# Example usage:
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
