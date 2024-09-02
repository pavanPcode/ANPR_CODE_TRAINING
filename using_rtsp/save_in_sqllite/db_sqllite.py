import sqlite3
from sqlite3 import Error

def insert_vehicle_transaction(vehiclenumber, vehicleimgpath, numberplateimgpath):
    try:
        # Connect to SQLite database
        conn = sqlite3.connect("anprresults.db")

        # Create a cursor object
        cursor = conn.cursor()

        # SQL query to insert data
        insert_query = """
        INSERT INTO VehicleTransactions (vehiclenumber, vehicleimgpath, numberplateimgpath)
        VALUES (?, ?, ?)
        """

        # Data to be inserted
        data = (vehiclenumber, vehicleimgpath, numberplateimgpath)

        # Execute the query
        cursor.execute(insert_query, data)

        # Commit the transaction
        conn.commit()

        print("Record inserted successfully.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()
