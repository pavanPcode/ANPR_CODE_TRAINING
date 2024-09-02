import mysql.connector
from mysql.connector import Error


def insert_vehicle_transaction(vehiclenumber, vehicleimgpath, numberplateimgpath):
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sadguru",
            database="anprresults"
        )

        if conn.is_connected():
            cursor = conn.cursor()

            # SQL query to insert data
            insert_query = """
            INSERT INTO VehicleTransactions (vehiclenumber, vehicleimgpath, numberplateimgpath)
            VALUES (%s, %s, %s)
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
        if conn.is_connected():
            cursor.close()
            conn.close()


