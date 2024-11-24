from ...config import get_db_connection
from flask import jsonify
import json


def create_preference_template(template_data):
    conn = get_db_connection()
    if conn is None:
        return (
            jsonify({"error": "internal error", "message": "server internal error"}),
            500,
        )
    required_fields = [
        "nurse_id",
        "template_name",
        "time_of_day",
        "hours_per_week",
        "preferred_week_days",
        "max_hours_per_shift",
        "hospitals_ranking",
    ]

    if not all(template_data.get(field) for field in required_fields):
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "Please provide complete form",
                }
            ),
            400,
        )

    try:
        nurse_id = template_data.get("nurse_id")
        template_name = template_data.get("template_name")
        time_of_day = template_data.get("time_of_day")
        hours_per_week = template_data.get("hours_per_week")
        max_hours_per_shift = template_data.get("max_hours_per_shift")
        preferred_week_days = json.dumps(template_data.get("preferred_week_days"))
        hospitals_ranking = json.dumps(template_data.get("hospitals_ranking"))
        fields = "nurse_id, template_name, time_of_day, hours_per_week, preferred_week_days, max_hours_per_shift, hospitals_ranking"
        values = "%s, %s, %s, %s, %s, %s, %s"
        cursor = conn.cursor()
        query = f"INSERT INTO preference_template ({fields}) VALUES ({values})"
        params = [
            nurse_id,
            template_name,
            time_of_day,
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
                    "msg": "Added Template Successfully",
                    "nurse_id": nurse_id,
                    "template_name": template_name,
                }
            ),
            200,
        )

    except Exception as e:
        conn.rollback() # Rollback the transaction if an error occurs
        return (jsonify({"error": str(e)}), 500)

    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
