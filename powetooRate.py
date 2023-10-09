import sqlite3
import csv

def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            item_name TEXT,
            ingredient_name TEXT,
            quantity REAL,
            unit TEXT,
            value REAL,
            catagory TEXT
        )
    ''')

def print_table_structure(cursor):
    table_name = input("Enter the table name to view its structure: ")
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print(f"Structure of table '{table_name}':")
    for column in columns:
        print(f"Column: {column[1]} - Type: {column[2]}")


def insert_data(cursor, item_name, ingredient_name, quantity, unit, value, catagory):
    cursor.execute('''
        INSERT INTO items (item_name, ingredient_name, quantity, unit, value, catagory)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (item_name, ingredient_name, quantity, unit, value, catagory))

def print_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Available tables:")
    for table in tables:
        print(table[0])

def rename_ingredients(cursor, old_name, new_name):
    cursor.execute("UPDATE items SET ingredient_name=? WHERE ingredient_name=?", (new_name, old_name))

def print_consolidated_item_names(cursor):
    cursor.execute("SELECT DISTINCT item_name FROM items")
    item_names = cursor.fetchall()
    print("Consolidated item_names:")
    for item_name in item_names:
        print(item_name[0])

def print_consolidated_ingredient_names(cursor):
    cursor.execute("SELECT DISTINCT ingredient_name FROM items")
    ingredient_names = cursor.fetchall()
    print("Consolidated ingredient_names:")
    for ingredient_name in ingredient_names:
        print(ingredient_name[0])

def main():
    print("This script manages CSV data in a database.")
    input("Press Enter to continue...")
    
    db_connection = sqlite3.connect('items.db')
    db_cursor = db_connection.cursor()

    create_table(db_cursor)

    while True:
        print("\nOptions:")
        print("1. Insert CSV data")
        print("2. Delete rows by item_name")
        print("3. Delete entire table")
        print("4. Rename ingredient_name")
        print("5. Print consolidated item_names")
        print("6. Print consolidated ingredient_names")
        print("7. Print available tables")
        print("8. See DB structure")
        print('9. To Exit')
        

        choice = input("Select an option: ")

        if choice == '1':
            with open('ing.csv', 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    item_name = row['item']
                    ingredient_name = row['Ing']
                    quantity = float(row['Qty']) if row['Qty'] else None
                    unit = row['unit'] if row['unit'] else None
                    value = row['value'] if row['value'] else None
                    catagory = row['catagory'] if row['catagory'] else None
                    insert_data(db_cursor, item_name, ingredient_name, quantity, unit, value, catagory)
            db_connection.commit()
            print("CSV data inserted successfully.")

        elif choice == '2':
            item_to_delete = input("Enter the item_name to delete rows: ")
            db_cursor.execute("DELETE FROM items WHERE item_name=?", (item_to_delete,))
            db_connection.commit()
            print(f"Rows with item_name '{item_to_delete}' deleted successfully.")

        elif choice == '3':
            db_cursor.execute("DROP TABLE IF EXISTS items")
            create_table(db_cursor)
            db_connection.commit()
            print("Table 'items' deleted and recreated successfully.")
        
        elif choice == '4':
            old_name = input("Enter the old ingredient_name: ")
            new_name = input("Enter the new ingredient_name: ")
            rename_ingredients(db_cursor, old_name, new_name)
            db_connection.commit()
            print("Ingredients renamed successfully.")

        elif choice == '5':
            print_consolidated_item_names(db_cursor)

        elif choice == '6':
            print_consolidated_ingredient_names(db_cursor)

        elif choice == '7':
            print_tables(db_cursor)

        elif choice == '8':
            print_table_structure(db_cursor)
        elif choice == '9':
            break


    db_connection.close()

if __name__ == "__main__":
    main()
