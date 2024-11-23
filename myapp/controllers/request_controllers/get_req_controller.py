from flask import jsonify, request
from ...config import get_db_connection
from datetime import date


def get_req():
    request_id = request.args.get("request_id")
    if not request_id:
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
        query = f"SELECT * FROM shift_request WHERE request_id = %s"
        params = [request_id]
        cursor.execute(query, params)
        found_req = cursor.fetchone()
        if not found_req:
            print("!!! No Preference Found")
            return (
                jsonify(
                    {
                        "error": "client-side issue",
                        "message": "No request found.",
                    }
                ),
                400,
            )

        print(found_req["shift_date"])
        print(type(found_req["shift_date"]))
        found_req["shift_date"] = found_req["shift_date"].strftime("%Y-%m-%d")
        # print(f"{date_str}, {type(date_str)}")
        return jsonify({"data": found_req}), 200

    except Exception as e:
        print(f"!!! error: {str(e)}")
        return (
            jsonify({"error": "internal error", "message": "server internal error"}),
            500,
        )
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
