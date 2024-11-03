from ..config import get_db_connection
from flask import jsonify, make_response
import bcrypt


def signup_user(user_data):
    conn = get_db_connection()
    if conn is None:
        return jsonify(
            jsonify({"error": "internal error", "message": "server internal error"}),
            500,
        )

    email = user_data.get("email")
    password = user_data.get("password")
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")
    role = user_data.get("role")

    if not (email and password and first_name and last_name and role):
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "Please provide complete form",
                }
            ),
            400,
        )

    cursor = conn.cursor()
    try:
        # Check for existing user
        check_query = "SELECT email FROM user WHERE email = %s"
        cursor.execute(check_query, (email,))
        if cursor.fetchone():
            return (
                jsonify(
                    {
                        "error": "client-side issue",
                        "message": "email already exists",
                    }
                ),
                409,
            )

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        # Insert new user
        query = """
        INSERT INTO user (email, password, first_name, last_name, role)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (email, hashed_password, first_name, last_name, role)
        cursor.execute(query, params)
        conn.commit()
        return jsonify({"email": email}), 200
    except Exception as e:
        conn.rollback()  # Rollback in case of any error
        return jsonify(
            jsonify({"error": "internal error", "message": "server internal error"}),
            500,
        )
    finally:
        cursor.close()
        conn.close()
