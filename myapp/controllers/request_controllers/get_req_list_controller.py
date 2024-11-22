from flask import jsonify, request
from ...config import get_db_connection
from datetime import datetime, timedelta


def get_req_list():
    supervisor_id = request.args.get("supervisor_id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    if not (supervisor_id and start_date and end_date):
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "data not provided",
                }
            ),
            400,
        )
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    if start_date_obj > end_date_obj:
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "check start/end dates",
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
        print(f"found hospital id: {hospital_id}")

        query = """
        SELECT * FROM shift_request
        WHERE hospital_id = %s AND shift_date BETWEEN %s AND %s
        """
        cursor.execute(query, (hospital_id, start_date, end_date))
        shift_requests = cursor.fetchall()
        # print(shift_requests)

        # Check if any records were found
        # if not shift_requests:
        #     return jsonify({"data": grouped_shifts}), 200

        # Initialize the dictionary
        grouped_shifts = {}
        delta = timedelta(days=1)
        while start_date_obj <= end_date_obj:
            date_str = start_date_obj.strftime("%Y-%m-%d")
            grouped_shifts[date_str] = []
            start_date_obj += delta
        # print(grouped_shifts)
        for request_dict in shift_requests:
            shift_date_str = request_dict["shift_date"].strftime("%Y-%m-%d")
            if shift_date_str in grouped_shifts:
                grouped_shifts[shift_date_str].append(request_dict)
        # print(grouped_shifts)

        return jsonify({"data": grouped_shifts}), 200

    except Exception as e:
        print(f"!!! error: {str(e)}")
        return (
            jsonify(
                {
                    "error": "internal error",
                    "message": "server internal error, finding hospital",
                }
            ),
            500,
        )
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
