from flask import jsonify, request
from ...config import get_db_connection
from datetime import datetime, timedelta
import math


def get_pref_template_list():
    page_size = request.args.get("page_size")
    current_page = request.args.get("current_page")
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
        count_query = (
            f"SELECT COUNT(*) as count FROM preference_template WHERE nurse_id=%s"
        )
        cursor.execute(count_query, (nurse_id,))
        count_result = cursor.fetchone()
        template_count = count_result["count"]
        print("count:", template_count)

        query = """
        SELECT * 
        FROM preference_template
        WHERE nurse_id = %s
        """
        query_values = [nurse_id]
        if current_page and page_size:
            page_size = int(page_size)
            current_page = int(current_page) - 1
            page_count = math.ceil(template_count / page_size)
            offset = current_page * page_size
            query += "ORDER BY template_id DESC LIMIT %s OFFSET %s"
            query_values = query_values + [page_size, offset]
            print(page_count)

        cursor.execute(query, query_values)
        template_list = cursor.fetchall()

        return (
            jsonify(
                {
                    "data": {
                        "template_list": template_list,
                        "page_count": page_count,
                        "current_page": current_page + 1,
                        "page_size": page_size,
                    }
                }
            ),
            200,
        )

    except Exception as e:
        conn.rollback()  # Rollback the transaction if an error occurs
        return (jsonify({"error": str(e)}), 500)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
