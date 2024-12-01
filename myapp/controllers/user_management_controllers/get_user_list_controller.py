from flask import jsonify, request
from ...config import get_db_connection
import math


def get_user_list():
    page_size = request.args.get("page_size")
    current_page = request.args.get("current_page")

    string_fields = ["email", "first_name", "last_name", "address", "phone_number"]
    other_fields = ["role", "seniority", "hospital_id"]
    conditions = []
    values = []

    for filter_field in string_fields:
        filter_value = request.args.get(filter_field)
        if filter_value is not None:
            conditions.append(f"{filter_field} LIKE %s")
            values.append(f"%{filter_value}%")

    for filter_field in other_fields:
        filter_value = request.args.get(filter_field)
        if filter_value is not None:
            conditions.append(f"{filter_field} = %s")
            values.append(filter_value)

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
        # Query to count total records for pagination
        count_query = f"SELECT COUNT(*) as total FROM user"
        if conditions:
            count_query += f" WHERE {' AND '.join(conditions)}"
        cursor.execute(count_query, values)
        count_result = cursor.fetchone()
        total_user_count = count_result["total"]

        # Calculate total pages
        total_page_num = 0

        query = f"""
            SELECT u_id, email, first_name, last_name, address, phone_number, birthday, role, seniority, hospital_id 
            FROM user
        """
        if len(conditions):
            query += f"WHERE {' AND '.join(conditions)}"

        if page_size and current_page:
            page_size = int(page_size)
            current_page = int(current_page)
            query += f" ORDER BY u_id ASC LIMIT %s OFFSET %s"
            offset = (current_page - 1) * page_size
            values = values + [page_size, offset]
            total_page_num = math.ceil(total_user_count / page_size)
        else:
            query += " ORDER BY u_id ASC"

        print(query)
        print(values)

        cursor.execute(query, values)
        users = cursor.fetchall()
        # count = len(users)

        return jsonify(
            {
                "data": {
                    "user_list": users,
                    "total_user_count": total_user_count,
                    "total_page_num": total_page_num,
                    "current_page": current_page,
                    "page_size": page_size,
                }
            }
        )
    except Exception as e:
        print(f"error quering DB:", e)
        return (
            jsonify({"error": "internal error", "message": "server internal error"}),
            500,
        )
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
