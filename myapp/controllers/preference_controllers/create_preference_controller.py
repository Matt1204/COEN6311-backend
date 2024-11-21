from ...config import get_db_connection
from flask import jsonify
import json


def create_preference(pref_data):
    conn = get_db_connection()
    if conn is None:
        return (
            jsonify({"error": "internal error", "message": "server internal error"}),
            500,
        )
    required_fields = [
        "nurse_id",
        "time_of_day",
        "start_date",
        "end_date",
        "hours_per_week",
        "preferred_week_days",
        "max_hours_per_shift",
        "hospitals_ranking",
    ]

    if not all(pref_data.get(field) for field in required_fields):
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "Please provide complete form",
                }
            ),
            400,
        )

    # params = []
    # for field in required_fields:
    #     val = pref_data.get(field)
    #     if val is None:
    #         print(f"{field} is None")
    #     else:
    #         if not val:
    #             print(f"{field} is empty str")
    #         else:
    #             print(f"{field}->{pref_data[field]} ({type(pref_data[field])})")

    try:
        nurse_id = pref_data.get("nurse_id")
        time_of_day = pref_data.get("time_of_day")
        start_date = pref_data.get("start_date")
        end_date = pref_data.get("end_date")
        hours_per_week = pref_data.get("hours_per_week")
        max_hours_per_shift = pref_data.get("max_hours_per_shift")
        preferred_week_days = json.dumps(pref_data.get("preferred_week_days"))
        hospitals_ranking = json.dumps(pref_data.get("hospitals_ranking"))
        fields = "nurse_id, time_of_day, start_date, end_date, hours_per_week, preferred_week_days, max_hours_per_shift, hospitals_ranking"
        values = "%s, %s, %s, %s, %s, %s, %s, %s"
        cursor = conn.cursor()
        query = f"INSERT INTO shift_preference ({fields}) VALUES ({values})"
        params = [
            nurse_id,
            time_of_day,
            start_date,
            end_date,
            hours_per_week,
            preferred_week_days,
            max_hours_per_shift,
            hospitals_ranking,
        ]
        cursor.execute(query, params)
        conn.commit()

        return (
            jsonify(
                {
                    "msg": "creation scuueccfuly",
                    "nurse_id": nurse_id,
                    "start_date": start_date,
                }
            ),
            200,
        )

    except Exception as e:
        print(e)
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
