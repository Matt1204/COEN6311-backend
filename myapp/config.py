from mysql.connector import connect, Error
import os

def get_db_connection():
    try:
        connection = connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )
        print("Database connection successful.")

        return connection
    except Error as e:
        # Here, you can log the error or handle it based on the type of error
        # For example, handle specific MySQL errors with custom messages
        if e.errno == 1045:  # Error code for "Access denied for user"
            print("Access denied: Check your username and password.")
        elif e.errno == 1049:  # Error code for "Unknown database"
            print("Database does not exist. Please check your database name.")
        elif e.errno == 2003:  # Error code for "Can't connect to MySQL server"
            print("Can't connect to the server. Check your host and port.")
        else:
            print(f"Error connecting to MySQL Platform: {e}")
        return None
