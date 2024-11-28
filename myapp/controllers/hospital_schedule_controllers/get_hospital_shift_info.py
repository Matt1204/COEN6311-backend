from flask import jsonify, request
from ...config import get_db_connection


def get_hospital_shift_info():
    request_id = request.args.get("request_id")

    if not request_id:
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
                    "error": "internal error",
                    "message": "internal error",
                }
            ),
            500,
        )
    cursor = conn.cursor(dictionary=True)

    try:
        # SQL query implementation
        shift_info_query = """
            SELECT
                COUNT(DISTINCT ms.shift_id) AS actual_nurse_num,
                ms.hospital_id,
                h.h_name as hospital_name,
                req.hours_per_shift,
                req.min_seniority min_seniority,
                ms.request_id,
                req.nurse_number AS request_nurse_num,
                ms.shift_date,
                req.shift_type as shift_type,
                sup.email as supervisor_email,
                sup.first_name as supervisor_firstname,
                sup.last_name as supervisor_lastname,
                ms.supervisor_id,

                req.day_of_week,
                sup.phone_number as supervisor_phone_number,
                sup.address as supervisor_address,
                h.h_address as hospital_address,
                h_hotline as hospital_hotline
            FROM 
                master_schedule ms
            JOIN
                hospital h ON ms.hospital_id = h.h_id
            JOIN
                shift_request req ON ms.request_id = req.request_id
            JOIN
                user sup ON ms.supervisor_id = sup.u_id
            WHERE
                ms.request_id = %s
            GROUP BY 
                ms.request_id,
                ms.shift_date,
                ms.supervisor_id,
                ms.hospital_id
        """
        cursor.execute(shift_info_query, (request_id,))
        shift_info = cursor.fetchone()
        shift_info["shift_date"] = shift_info["shift_date"].strftime("%Y-%m-%d")

        if not shift_info:
            print("!!! No shift Found")
            return (
                jsonify(
                    {
                        "error": "client-side issue",
                        "message": "No shift found.",
                    }
                ),
                400,
            )

        nurse_list_query = """
            SELECT 
                ms.request_id,
                
                ms.nurse_id,
                nur.email as nurse_email,
                nur.first_name as nurse_firstname,
                nur.last_name as nurse_lastname,
                nur.seniority as nurse_seniority,
                
                nur.address as nurse_address,
                nur.phone_number as nurse_phone_number,
                nur.birthday as nurse_birthday

            
            FROM 
                master_schedule ms
            JOIN
                hospital h ON ms.hospital_id = h.h_id
            JOIN
                shift_request req ON ms.request_id = req.request_id
            JOIN
                user nur ON ms.nurse_id = nur.u_id
            WHERE 
            ms.request_id = %s
        """
        cursor.execute(nurse_list_query, (request_id,))
        nurse_list = cursor.fetchall()
        if not nurse_list:
            print("!!! No nurse Found")
            return (
                jsonify(
                    {
                        "error": "client-side issue",
                        "message": "No nurse found in the shift.",
                    }
                ),
                400,
            )

        for nurse in nurse_list:
            if nurse["nurse_birthday"]:
                nurse["nurse_birthday"] = nurse["nurse_birthday"].strftime("%Y-%m-%d")
        return (
            jsonify({"data": {"shift_info": shift_info, "nurse_list": nurse_list}}),
            200,
        )

    except Exception as e:
        print(f"Error during query execution: {str(e)}")
        return (
            jsonify(
                {
                    "error": "internal error",
                    "message": "An error occurred while fetching data.",
                }
            ),
            500,
        )

    finally:
        # Ensure proper cleanup
        if "cursor" in locals() and cursor:
            cursor.close()
        if "conn" in locals() and conn:
            conn.close()
