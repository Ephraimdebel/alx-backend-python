#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator to fetch rows from user_data in batches."""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    offset = 0
    while True:
        cursor.execute(
            "SELECT * FROM user_data LIMIT %s OFFSET %s",
            (batch_size, offset)
        )
        batch = cursor.fetchall()
        if not batch:
            break
        yield batch
        offset += batch_size

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Process each batch and filter users over the age of 25"""
    for batch in stream_users_in_batches(batch_size):  # 1st loop
        for user in batch:  # 2nd loop
            if user['age'] > 25:
                print(user)  # output or process user
