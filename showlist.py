import sqlite3

def print_sqlite_database(database_path):
    # Connect to the SQLite database
    db_connection = sqlite3.connect(database_path)
    db_cursor = db_connection.cursor()

    # Get a list of all tables in the database
    db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = db_cursor.fetchall()

    # Iterate through each table and print its contents
    for table_name in table_names:
        table_name = table_name[0]  # Extract the table name from the result tuple
        print(f"Table: {table_name}")

        # Fetch all rows from the current table
        db_cursor.execute(f"SELECT * FROM {table_name};")
        rows = db_cursor.fetchall()

        # Print the column names
        column_names = [description[0] for description in db_cursor.description]
        print(", ".join(column_names))

        # Print the rows
        for row in rows:
            print(", ".join(str(value) for value in row))

        print("\n")

    # Close the database connection
    db_connection.close()

# Example usage:
# Replace 'items.db' with the path to your SQLite database file
print_sqlite_database('items.db')
