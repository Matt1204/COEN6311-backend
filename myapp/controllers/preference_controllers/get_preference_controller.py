from flask import jsonify, request
from ...config import get_db_connection


def get_preference():
    nurse_id = request.args.get("nurse_id")
    start_date = request.args.get("start_date")

    if not nurse_id or not start_date:
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "email/date not provided",
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

    try:
        return_string = "nurse_id, time_of_day, start_date, end_date, hours_per_week, preferred_week_days, max_hours_per_shift, hospitals_ranking"
        query = f"SELECT {return_string} FROM shift_preference WHERE nurse_id = %s AND start_date = %s"
        params = [nurse_id, start_date]
        cursor.execute(query, params)
        found_pref = cursor.fetchone()
        print(found_pref)
        if found_pref is None:
            print("!!! No Preference Found")
            return (
                jsonify({"data": {}}),
                200,
            )

        # userData = foundUser
        # return jsonify({"data": "found_pref"}), 200
        return jsonify({"data": found_pref}), 200

    except Exception as e:
        # Handle general exceptions
        print(e)
        return (
            jsonify({"error": "internal error", "message": "server internal error"}),
            500,
        )
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
