from flask import jsonify, request
from ...config import get_db_connection


def create_req(req_payload):
    required_fields = [
        "supervisor_id",
        "shift_date",
        "shift_type",
        "hours_per_shift",
        "day_of_week",
        "nurse_number",
        "min_seniority",
    ]

    # Check if all required fields are present in the payload
    if not all(req_payload.get(field) for field in required_fields):
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "data not provided",
                }
            ),
            400,
        )

    conn = get_db_connection()
    if conn is None:
        return (
            jsonify(
                {
                    "error": "Database Error",
                    "message": "Failed to connect to the database.",
                }
            ),
            500,
        )

    cursor = conn.cursor(dictionary=True)

    try:
        # Ensure the supervisor exists and find their hospital ID
        supervisor_id = req_payload["supervisor_id"]
        cursor.execute("SELECT hospital_id FROM user WHERE u_id = %s", (supervisor_id,))
        found_hid = cursor.fetchone()
        if not found_hid:
            return (
                jsonify(
                    {
                        "error": "Invalid Supervisor",
                        "message": "No hospital associated with the provided supervisor_id.",
                    }
                ),
                400,
            )

        # Insert the new shift request using parameters from the payload
        hospital_id = found_hid["hospital_id"]
        query = """
        INSERT INTO shift_request (hospital_id, supervisor_id, shift_date, shift_type, hours_per_shift, day_of_week, nurse_number, min_seniority)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            hospital_id,
            supervisor_id,
            req_payload["shift_date"],
            req_payload["shift_type"],
            req_payload["hours_per_shift"],
            req_payload["day_of_week"],
            req_payload["nurse_number"],
            req_payload["min_seniority"],
        )
        cursor.execute(query, params)
        conn.commit()

        return jsonify({"message": "Shift request created successfully"}), 201

    except Exception as e:
        conn.rollback()  # Rollback in case of error
        print(f"Error: {str(e)}")  # Log the error for debugging
        return (
            jsonify(
                {
                    "error": "Server Error",
                    "message": "An error occurred while processing the request.",
                }
            ),
            500,
        )

    finally:
        cursor.close()
        conn.close()
