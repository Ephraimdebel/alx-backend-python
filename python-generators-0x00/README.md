# Python Generators: Streaming Rows from a MySQL Database

## Project Overview
This project demonstrates the use of **Python generators** to stream rows from a MySQL database efficiently. By leveraging generators, data is fetched one row at a time, which reduces memory usage and allows handling of large datasets.

The project includes scripts to:
- Connect to the MySQL server
- Create a database and table
- Insert data from a CSV file
- Stream rows using a generator function

## Database Schema
The project uses a MySQL database `ALX_prodev` with a table `user_data`:

| Column   | Type    | Constraints                     |
|----------|---------|--------------------------------|
| user_id  | UUID    | Primary Key, Indexed           |
| name     | VARCHAR | NOT NULL                       |
| email    | VARCHAR | NOT NULL                       |
| age      | DECIMAL | NOT NULL                       |

## Files
- `seed.py` : Contains all functions for database connection, table creation, data insertion, and generator for streaming rows.
- `user_data.csv` : Sample data to populate the `user_data` table.
- `0-main.py` : Example script demonstrating the usage of the generator.

## Key Functions in `seed.py`
- `connect_db()` : Connects to the MySQL server.
- `create_database(connection)` : Creates the `ALX_prodev` database if it doesn’t exist.
- `connect_to_prodev()` : Connects to the `ALX_prodev` database.
- `create_table(connection)` : Creates the `user_data` table if it doesn’t exist.
- `insert_data(connection, csv_file)` : Inserts rows from CSV into the database.
- `stream_rows(connection)` : Generator function that fetches rows one at a time.

## Usage
1. Ensure MySQL server is running.
2. Update `seed.py` with your MySQL credentials.
3. Run the main script:
   ```bash
   ./0-main.py
The script will create the database and table, insert sample data, and demonstrate streaming rows using a generator.

Benefits of Generators

Memory Efficiency: Fetches one row at a time.

Lazy Evaluation: Only computes values when needed.

Scalable: Ideal for large datasets where loading all data at once is not feasible.

Example Output
{'user_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67}
{'user_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119}
...