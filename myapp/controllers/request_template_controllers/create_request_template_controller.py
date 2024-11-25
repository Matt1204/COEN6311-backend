from ...config import get_db_connection
from flask import jsonify
import json


def create_request_template(template_data):
    conn = get_db_connection()
    if conn is None:
        return (
            jsonify({"error": "internal error", "message": "server internal error"}),
            500,
        )
    required_fields = [
        "hospital_id",
        "supervisor_id",
        "template_name",
        "shift_type",
        "hours_per_shift",
        "nurse_number",
        "min_seniority"
    ]

    if not all(template_data.get(field) for field in required_fields):
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "Please provide complete form",
                    "missing_fields": [
                        field for field in required_fields if not template_data.get(field)
                    ],
                }
            ),
            400,
        )

    try:
        hospital_id = template_data.get("hospital_id")
        supervisor_id = template_data.get("supervisor_id")
        template_name = template_data.get("template_name")
        shift_type = template_data.get("shift_type")
        hours_per_shift = template_data.get("hours_per_shift")
        nurse_number = template_data.get("nurse_number")
        min_seniority = template_data.get("min_seniority")

        fields = "hospital_id, supervisor_id, template_name, shift_type, hours_per_shift, nurse_number, min_seniority"
        values = "%s, %s, %s, %s, %s, %s, %s"
        cursor = conn.cursor()
        query = f"INSERT INTO request_template ({fields}) VALUES ({values})"
        params = [
            hospital_id,
            supervisor_id,
            template_name,
            shift_type,
            hours_per_shift,
            nurse_number,
            min_seniority,
        ]
        cursor.execute(query, params)
        conn.commit()

        return (
            jsonify(
                {
                    "msg": "Added Template Successfully",
                    "hospital_id": hospital_id,
                    "supervisor_id": supervisor_id,
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
