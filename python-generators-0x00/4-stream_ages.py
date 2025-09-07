#!/usr/bin/python3
seed = __import__('seed')


def stream_user_ages():
    """Generator that yields user ages one by one from the database."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']  # yield one age at a time
    cursor.close()
    connection.close()


def calculate_average_age():
    """Use the generator to compute average age without loading all data at once."""
    total = 0
    count = 0
    for age in stream_user_ages():  # loop 1: iterate generator
        total += age
        count += 1

    if count > 0:
        average = total / count
        print(f"Average age of users: {average}")
    else:
        print("No users found.")


if __name__ == "__main__":
    calculate_average_age()
