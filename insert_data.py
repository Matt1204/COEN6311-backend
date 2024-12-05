import mysql.connector
from mysql.connector import Error
import bcrypt
import random
import json
import datetime
from faker import Faker


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


def populate_nurse(connection):
    password = "11111111"
    # bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    try:
        fake = Faker()
        insert_query = """
        INSERT INTO user (first_name, last_name, email, password, address, phone_number, birthday, role, seniority)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor = connection.cursor()

        # for _ in range(5):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"nurse-{first_name.lower()}{last_name.lower()}@mail.com"
        password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )
        address = fake.address().replace(
            "\n", " "
        )  # Replace newlines in addresses if any
        phone_number = fake.phone_number()
        birthday = fake.date_of_birth(minimum_age=25, maximum_age=55)
        role = "nurse"
        seniority = random.randint(5, 10)
        params = [
            first_name,
            last_name,
            email,
            password,
            address,
            phone_number,
            birthday,
            role,
            seniority,
        ]
        print(params)
        cursor.execute(insert_query, params)

        connection.commit()
        cursor.close()
        print(f"nurses populated successfully.")
    except Error as err:
        print(f"Error: '{err}'")


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


def populate_request(connection, start_date, end_date):
    cursor = connection.cursor()

    # get supervisors and their affiliated hospitals
    get_supervisor_query = """
        SELECT u_id, hospital_id
        FROM user
        WHERE role = 'supervisor'
    """
    cursor.execute(get_supervisor_query)
    supervisors = cursor.fetchall()
    # print(supervisors)
    # save a list of each hospital's supervisors
    hospital_supervisors = {}
    for supervisor in supervisors:
        if supervisor[1] not in hospital_supervisors:
            hospital_supervisors[supervisor[1]] = []
        hospital_supervisors[supervisor[1]].append(supervisor[0])
    print(hospital_supervisors)
    # {1: [id, id], 2:[id, id, ...], 3:[id...] }
    shift_type_options = ["morning", "afternoon", "night"]

    # Populate the shift_request table, we need to delete the previous entries for the start_date week first.
    # We need 3 shifts per day for each hospital, doesn't matter if the same supervisor is assigned to multiple shifts.
    # We need to populate the table for the whole week starting from start_date.
    # The hours per shift is 8 hours, the nurse number is 40, the minimum seniority is a random number from 1 to 10 inclusive.
    # The day of the week is the day of the week of the shift_date.

    # Delete previous entries for the start_date week
    delete_query = "DELETE FROM shift_request WHERE shift_date BETWEEN %s AND %s"
    cursor.execute(delete_query, (start_date, end_date))
    connection.commit()

    current_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    while current_date <= end_date:
        day_of_week = current_date.strftime("%A")
        # print(day_of_week)
        for hospital_id, supervisors in hospital_supervisors.items():
            for shift_type in shift_type_options:
                supervisor_id = random.choice(supervisors)
                min_seniority = random.randint(1, 9)
                nurse_number = random.randint(2, 9)
                insert_query = """
                    INSERT INTO shift_request (hospital_id, supervisor_id, shift_type, hours_per_shift, nurse_number, min_seniority, shift_date, day_of_week)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = [
                    hospital_id,
                    supervisor_id,
                    shift_type,
                    8,
                    nurse_number,
                    min_seniority,
                    current_date.strftime("%Y-%m-%d"),
                    day_of_week,
                ]
                cursor.execute(insert_query, params)
        current_date += datetime.timedelta(days=1)

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
        # populate_preference(connection, "2024-12-23", "2024-12-29")
        populate_request(connection, "2024-12-23", "2024-12-29")
        # for _ in range(15):
        #     populate_nurse(connection)
    # Close the connection
    if connection:
        connection.close()


if __name__ == "__main__":
    main()
