"""
    "hours_per_shift" in "shift_request" table 
    is hardcoded to 8 due to Algorithm Limitation  !!!!!!!!!!!
"""

from flask import jsonify, request
from ...config import get_db_connection
import json


def update_req(req_payload):
    request_id = request.args.get("request_id")
    if not request_id:
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "request_id not provided",
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
        found_pref = cursor.fetchone()
        print(found_pref)
        if found_pref is None:
            print("request not found!!!")
            return (
                jsonify(
                    {
                        "error": "client-side issue",
                        "message": "request not found",
                    }
                ),
                404,
            )
    except Exception as e:
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "error finding request",
                }
            ),
            400,
        )

    all_fields = [
        "supervisor_id",
        "shift_date",
        "shift_type",
        "day_of_week",
        "hours_per_shift",
        "min_seniority",
        "nurse_number",
    ]
    updates = []
    params = {"request_id": request_id}
    for field in all_fields:
        value = req_payload.get(field)
        print(f"- {field} => {value}({type(value)})")
        if value is not None:
            # print(f"!{field} provided")
            updates.append(f"{field} = %({field})s")
            if type(value) is str:
                params[field] = value
            else:
                params[field] = json.dumps(value)

            # "hours_per_shift" in "shift_request" table hardcoded to 8 due to Algorithm Limitation  !!!!!!!!!!!
            if field == "hours_per_shift":
                params[field] = 8

    if not updates:
        # return jsonify({"message": "No valid fields provided to update"}), 400
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "payload empty",
                }
            ),
            400,
        )
    print(updates)
    print(params)

    try:
        query = (
            "UPDATE shift_request SET "
            + ", ".join(updates)
            + " WHERE request_id = %(request_id)s"
        )
        print(query)

        cursor.execute(query, params)
        conn.commit()  # Commit the transaction
        return jsonify({"message": "update successful"}), 200

    except Exception as e:
        # Handle general exceptions
        print(e)
        return (
            jsonify(
                jsonify({"error": "internal error", "message": "server internal error"})
            ),
            500,
        )
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
