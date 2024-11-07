from flask import jsonify, make_response, request
from ...config import get_db_connection


def get_all_hospitals():
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

    return_fields = "h_id, h_name, h_address, h_hotline"
    try:
        cursor.execute(f"SELECT {return_fields} FROM hospital")
        hospitals = cursor.fetchall()  # Fetch all rows from the database
        return jsonify({"data": hospitals})  # Return the list of hospitals as JSON
    except Exception as e:
        # Handle general exceptions
        print("get_all_hospitals error: " + e)
        return jsonify(
            jsonify({"error": "internal error", "message": "server internal error"}),
            500,
        )
    finally:
        cursor.close()
        conn.close()
