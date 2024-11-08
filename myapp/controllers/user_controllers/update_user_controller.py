from flask import jsonify, make_response, request
from ...config import get_db_connection
from pymysql import MySQLError, OperationalError, IntegrityError


def update_user(req_payload):
    email = request.args.get("email")
    if not email:
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "email not provided",
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
        check_query = "SELECT email FROM user WHERE email = %s"
        cursor.execute(check_query, (email,))
        if not cursor.fetchone():
            return (
                jsonify(
                    {
                        "error": "client-side issue",
                        "message": "email doesn't exists",
                    }
                ),
                404,
            )
    except Exception as e:
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "check",
                }
            ),
            400,
        )

    all_fields = [
        "first_name",
        "last_name",
        "address",
        "phone_number",
        "birthday",
        "seniority",
        "hospital_id",
    ]
    updates = []
    params = {"email": email}
    for field in all_fields:
        value = req_payload.get(field)
        print(f"{field}: {value}")
        if value is not None:
            print(f"{field} in")
            updates.append(f"{field} = %({field})s")
            params[field] = req_payload.get(field)

    if not updates:
        # return jsonify({"message": "No valid fields provided to update"}), 400
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "No valid fields provided to update",
                }
            ),
            400,
        )

    sql = "UPDATE user SET " + ", ".join(updates) + " WHERE email = %(email)s"
    # print(updates)
    # print(params)
    print(sql)

    try:
        cursor.execute(sql, params)
        conn.commit()  # Commit the transaction

        params.pop("email", None)
        return jsonify({"data": {"email": email}}), 200

    except IntegrityError as e:
        conn.rollback()
        return jsonify({"error": "Integrity error", "message": str(e)}), 400
    except OperationalError as e:
        conn.rollback()
        return jsonify({"error": "Operational error", "message": str(e)}), 500
    except MySQLError as e:
        conn.rollback()
        return jsonify({"error": "Database error", "message": str(e)}), 500
    except Exception as e:
        if conn:
            conn.rollback()  # Rollback in case of error
        return (
            jsonify(
                {"error": "Internal server error", "message": "check data validity"}
            ),
            400,
        )
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
