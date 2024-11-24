from flask import jsonify, request
from ...config import get_db_connection


def get_request_template():
    template_id = request.args.get("template_id")

    if not template_id:
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "template_id not provided",
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
        return_string = "hospital_id, template_name, shift_type, hours_per_shift, nurse_number, min_seniority"
        query = f"SELECT {return_string} FROM request_template WHERE template_id = %s"
        params = [template_id]
        cursor.execute(query, params)
        found_template = cursor.fetchone()
        print(found_template)
        if found_template is None:
            print("!!! No Request Template Found")
            return (
                jsonify({"data": {}}),
                200,
            )

        # userData = foundUser
        # return jsonify({"data": "found_pref"}), 200
        return jsonify({"data": found_template}), 200

    except Exception as e:
        conn.rollback() # Rollback the transaction if an error occurs
        return (jsonify({"error": str(e)}), 500)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
