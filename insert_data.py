import mysql.connector
from mysql.connector import Error
import bcrypt
import random
import json


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


def populate_preference(connection, start_date, end_date):
    cursor = connection.cursor()

    get_nurse_query = """
        SELECT u_id 
        FROM user
        WHERE role = 'nurse'
    """
    cursor.execute(get_nurse_query)
    nurses_id_list = cursor.fetchall()
    # print(nurses_id_list)

    time_of_day_options = ["morning", "afternoon", "night"]
    week_days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    delete_query = "DELETE FROM shift_preference WHERE start_date = %s"
    cursor = connection.cursor()
    cursor.execute(delete_query, (start_date,))
    connection.commit()

    for nurse_id in nurses_id_list:
        # print(nurse_id[0])

        insert_query = """
            INSERT INTO shift_preference (nurse_id, time_of_day, start_date, end_date, hours_per_week, preferred_week_days, max_hours_per_shift, hospitals_ranking)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        time_of_day = random.choice(time_of_day_options)
        preferred_days = json.dumps(random.sample(week_days, k=random.randint(1, 7)))
        hospitals_ranking = [1, 2, 3]
        random.shuffle(hospitals_ranking)
        hospitals_ranking_json = json.dumps(hospitals_ranking)
        params = [
            nurse_id[0],
            time_of_day,
            start_date,
            end_date,
            40,
            preferred_days,
            8,
            hospitals_ranking_json,
        ]
        # print(insert_query)
        # print(params)
        cursor.execute(insert_query, params)

    connection.commit()
    cursor.close()


def main():
    # Database connection parameters
    host = "localhost"
    port = "3306"
    user = "root"
    db_password = "123456"
    database = "coen6311"

    connection = create_database_connection(host, port, user, db_password, database)

    # Execute nurse inserts
    if connection:
        # execute_query(connection, nurse_inserts)
        populate_preference(connection, "2024-12-16", "2024-12-22")

    # Close the connection
    if connection:
        connection.close()


if __name__ == "__main__":
    main()
