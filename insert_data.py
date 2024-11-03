import mysql.connector
from mysql.connector import Error
import bcrypt


def create_database_connection(host_name, port, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            port=port,
            user=user_name,
            passwd=user_password,
            database=db_name,
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def main():
    # Database connection parameters
    host = "localhost"
    port = "3306"
    user = "root"
    db_password = "123456"
    database = "coen6311"

    # Create a database connection
    connection = create_database_connection(host, port, user, db_password, database)

    # SQL commands to create and populate the 'hospital' table
    # hospital_inserts = """
    # INSERT INTO `hospital` (h_name, h_address, h_hotline)
    # VALUES
    # ('Hospital One', '1234 Med Street', '123-456-7890'),
    # ('Hospital Two', '5678 Health Ave', '234-567-8901'),
    # ('Hospital Three', '9101 Care Blvd', '345-678-9012');
    # """
    # # Execute hospital inserts
    # if connection:
    #     execute_query(connection, hospital_inserts)

    # Nurses and supervisors data insertion
    password = "11111111"
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    nurse_inserts = f"""
    INSERT INTO `user` (first_name, last_name, email, password, role, hospital_id, created_at, updated_at)
    VALUES 
        ('supervisor01_firstname', 'supervisor01_lastname', 'supervisor01@mail.com', '{bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")}', 'supervisor', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        ('supervisor02_firstname', 'supervisor02_lastname', 'supervisor02@mail.com', '{bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")}', 'supervisor', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        ('supervisor03_firstname', 'supervisor03_lastname', 'supervisor03@mail.com', '{bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")}', 'supervisor', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        ('supervisor04_firstname', 'supervisor04_lastname', 'supervisor04@mail.com', '{bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")}', 'supervisor', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        ('supervisor05_firstname', 'supervisor05_lastname', 'supervisor05@mail.com', '{bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")}', 'supervisor', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        ('supervisor06_firstname', 'supervisor06_lastname', 'supervisor06@mail.com', '{bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")}', 'supervisor', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
          """
    print(nurse_inserts)

    # Execute nurse inserts
    if connection:
        execute_query(connection, nurse_inserts)

    # Close the connection
    if connection:
        connection.close()


if __name__ == "__main__":
    main()
