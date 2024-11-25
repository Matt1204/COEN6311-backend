from flask import jsonify, request
from ...config import get_db_connection
from datetime import datetime, timedelta


def get_preference_templates():
    nurse_id = request.args.get("nurse_id")
    if not (nurse_id):
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "nurse_id not provided",
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
        query = """
        SELECT * FROM preference_template
        WHERE nurse_id = %s
        """
        cursor.execute(query, (nurse_id,))
        preference_templates = cursor.fetchall()

        return jsonify({"data": preference_templates}), 200

    except Exception as e:
        conn.rollback() # Rollback the transaction if an error occurs
        return (jsonify({"error": str(e)}), 500)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
