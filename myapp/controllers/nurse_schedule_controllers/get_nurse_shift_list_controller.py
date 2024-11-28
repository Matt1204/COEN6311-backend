from flask import jsonify, request
from ...config import get_db_connection
from datetime import datetime, timedelta


def get_nurse_shift_list():
    nurse_id = request.args.get("nurse_id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if not (nurse_id and start_date and end_date):
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
        # SQL query implementation
        query = """
            SELECT
                ms.shift_id,
                ms.shift_date,
                ms.request_id,
                ms.nurse_id,
                h.h_id AS hospital_id,
                h.h_name AS hospital_name,
                h.h_address AS hospital_address,
                h.h_hotline AS hospital_hotline,
                req.shift_type,
                req.hours_per_shift
            FROM 
                master_schedule ms
            JOIN
                hospital h ON ms.hospital_id = h.h_id
            JOIN
                shift_request req ON ms.request_id = req.request_id
            WHERE
                ms.shift_date BETWEEN %s AND %s
                AND ms.nurse_id = %s;
        """
        cursor.execute(query, (start_date, end_date, nurse_id))
        results = cursor.fetchall()

        for shift in results:
            # print(shift["shift_date"])
            shift["shift_date"] = shift["shift_date"].strftime("%Y-%m-%d")

        grouped_shifts = {}
        delta = timedelta(days=1)
        while start_date_obj <= end_date_obj:
            date_str = start_date_obj.strftime("%Y-%m-%d")
            grouped_shifts[date_str] = []
            start_date_obj += delta
        # print(grouped_shifts)
        for shift_dict in results:
            shift_date_str = shift_dict["shift_date"]
            if shift_date_str in grouped_shifts:
                grouped_shifts[shift_date_str].append(shift_dict)

        # if not results:
        #     # return jsonify({"message": "No shifts found for the given criteria"}), 404
        #     return jsonify({"data": {}}), 200

        # print(results)
        return jsonify({"data": grouped_shifts}), 200

    except Exception as e:
        print(f"!!! error: {str(e)}")
        return (
            jsonify(
                {
                    "error": "internal error",
                    "message": "server internal error finding shifts",
                }
            ),
            500,
        )
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
