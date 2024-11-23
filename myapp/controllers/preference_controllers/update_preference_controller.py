from flask import jsonify, request
from ...config import get_db_connection
import json


def update_pref(pref_data):
    nurse_id = request.args.get("nurse_id")
    start_date = request.args.get("start_date")
    if not nurse_id or not start_date:
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "email/start_date not provided",
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
        query = f"SELECT preference_id FROM shift_preference WHERE nurse_id = %s AND start_date = %s"
        params = [nurse_id, start_date]
        cursor.execute(query, params)
        found_pref = cursor.fetchone()
        print(found_pref)
        if found_pref is None:
            print("pref not found!!!")
            return (
                jsonify(
                    {
                        "error": "client-side issue",
                        "message": "preference not found",
                    }
                ),
                404,
            )
    except Exception as e:
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "error finding preference",
                }
            ),
            400,
        )

    all_fields = [
        "time_of_day",
        "hours_per_week",
        "preferred_week_days",
        "max_hours_per_shift",
        "hospitals_ranking",
    ]
    updates = []
    params = {"nurse_id_identifier": nurse_id, "start_date_identifier": start_date}
    for field in all_fields:
        value = pref_data.get(field)
        print(f"- {field} => {value}({type(value)})")
        if value is not None:
            # print(f"!{field} provided")
            updates.append(f"{field} = %({field})s")
            if type(value) is str:
                params[field] = value
            else:
                params[field] = json.dumps(value)

    # print(updates)
    print(params)
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

    try:
        sql = (
            "UPDATE shift_preference SET "
            + ", ".join(updates)
            + " WHERE nurse_id = %(nurse_id_identifier)s AND start_date = %(start_date_identifier)s"
        )

        cursor.execute(sql, params)
        conn.commit()  # Commit the transaction
        return jsonify({"msg": "update successful"}), 200

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
