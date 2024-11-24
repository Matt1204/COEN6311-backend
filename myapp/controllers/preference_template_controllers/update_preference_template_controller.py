from flask import jsonify, request
from ...config import get_db_connection
import json


def update_preference_template(template_data):
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
        query = f"SELECT template_name FROM preference_template WHERE template_id = %s"
        params = [template_id]
        cursor.execute(query, params)
        found_template= cursor.fetchone()
        # print(found_template)
        if found_template is None:
            print("template not found!!!")
            return (
                jsonify(
                    {
                        "error": "client-side issue",
                        "message": "template not found",
                    }
                ),
                404,
            )
    except Exception as e:
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "error finding template",
                }
            ),
            400,
        )

    all_fields = [
        "template_name",
        "time_of_day",
        "hours_per_week",
        "preferred_week_days",
        "max_hours_per_shift",
        "hospitals_ranking",
    ]
    updates = []
    params = {"template_id": template_id}
    for field in all_fields:
        value = template_data.get(field)
        # print(f"- {field} => {value}({type(value)})")
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
            "UPDATE preference_template SET "
            + ", ".join(updates)
            + " WHERE template_id = %(template_id)s"
        )

        cursor.execute(sql, params)
        conn.commit()  # Commit the transaction
        return jsonify({"msg": "template updated successful"}), 200

    except Exception as e:
        conn.rollback() # Rollback the transaction if an error occurs
        return (jsonify({"error": str(e)}), 500)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
