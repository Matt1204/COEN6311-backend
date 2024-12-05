from flask import jsonify, make_response, request
from ...config import get_db_connection


def get_user():
    email = request.args.get("email")
    u_id = request.args.get("u_id")
    if not u_id:
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "u_id not provided",
                }
            ),
            400,
        )

    conn = get_db_connection()
    if conn is None:
        return (
            jsonify(
                {
                    "error": "internal error",
                    "message": "internal error",
                }
            ),
            500,
        )
    cursor = conn.cursor(dictionary=True)

    return_string = "first_name, last_name, email, address, phone_number, birthday, seniority, hospital_id"
    try:
        cursor.execute(f"SELECT {return_string} FROM user WHERE u_id = %s", (u_id,))
        foundUser = cursor.fetchone()
        if foundUser is None:
            return (
                jsonify(
                    {
                        "error": "account not found",
                        "message": "Incorrect Email",
                    }
                ),
                404,
            )

        userData = foundUser
        return jsonify({"data": foundUser}), 200

    except Exception as e:
        # Handle general exceptions
        print(e)
        return (
            jsonify({"error": "internal error", "message": "server internal error"}),
            500,
        )
    finally:
        cursor.close()
        conn.close()
