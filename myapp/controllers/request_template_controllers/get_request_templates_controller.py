from flask import jsonify, request
from ...config import get_db_connection


def get_request_templates():
    supervisor_id = request.args.get("supervisor_id")
    if not (supervisor_id):
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "supervisor_id not provided",
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
        cursor.execute("SELECT hospital_id FROM user WHERE u_id = %s", (supervisor_id,))
        found_hid = cursor.fetchone()
        if not found_hid:
            print("hospital NOT found")
            return (
                jsonify(
                    {
                        "error": "Invalid supervisor_id",
                        "message": "No hospital found for the given supervisor_id.",
                    }
                ),
                400,
            )
        hospital_id = found_hid["hospital_id"]

        query = """
        SELECT * FROM request_template
        WHERE hospital_id = %s
        """
        cursor.execute(query, (hospital_id,))
        request_templates = cursor.fetchall()

        return jsonify({"data": request_templates}), 200

    except Exception as e:
        conn.rollback() # Rollback the transaction if an error occurs
        return (jsonify({"error": str(e)}), 500)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
