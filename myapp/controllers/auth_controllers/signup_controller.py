from ...config import get_db_connection
from flask import jsonify, make_response
import bcrypt


def signup_user(user_data):
    conn = get_db_connection()
    if conn is None:
        return (
            jsonify({"error": "internal error", "message": "server internal error"}),
            500,
        )

    required_fields = ["email", "password", "first_name", "last_name", "role"]
    if not all(user_data.get(field) for field in required_fields):
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "Please provide complete form",
                }
            ),
            400,
        )

    email = user_data.get("email")
    password = user_data.get("password")
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")
    role = user_data.get("role")

    seniority = user_data.get("seniority")
    hospital_id = user_data.get("hospital_id")
    if role == "nurse" and (not seniority or hospital_id):
        return (
            jsonify(
                {"error": "client-side issue", "message": "Please provide correct form"}
            ),
            400,
        )
    if role == "supervisor" and (not hospital_id or seniority):
        return (
            jsonify(
                {"error": "client-side issue", "message": "Please provide correct form"}
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

        fields = "email, password, first_name, last_name, role"
        values = "%s, %s, %s, %s, %s"
        params = [email, hashed_password, first_name, last_name, role]
        if seniority:
            fields += ", seniority"
            values += ", %s"
            params.append(seniority)

        if hospital_id:
            fields += ", hospital_id"
            values += ", %s"
            params.append(hospital_id)

        # Insert new user
        query = f"INSERT INTO user ({fields}) VALUES ({values})"
        cursor.execute(query, params)
        conn.commit()
        return jsonify({"email": email}), 200
    except Exception as e:
        conn.rollback()  # Rollback in case of any error
        return (
            jsonify({"error": "internal error", "message": "server internal error"}),
            500,
        )

    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
