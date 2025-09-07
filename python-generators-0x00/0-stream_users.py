#!/usr/bin/python3
import mysql.connector

def stream_users():
    """Generator function that yields rows from the user_data table one by one"""
    
    # Connect to your database (update credentials as needed)
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)  # dictionary=True returns rows as dicts

    # Execute query to fetch all users
    cursor.execute("SELECT * FROM user_data")

    # Yield rows one by one
    for row in cursor:
        yield row

    # Close resources
    cursor.close()
    connection.close()
