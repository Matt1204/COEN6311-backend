from ...config import get_db_connection
from flask import jsonify, request

def delete_preference_template():
    template_id = request.args.get("template_id")

    if not template_id:
        return (jsonify({"error": "Please provide template_id"}), 400)

    conn = get_db_connection()
    if conn is None:
        return (
            jsonify({"error": "internal error", "message": "server internal error"}),
            500,
        )
    
    try:
        cursor  = conn.cursor()

        cursor.execute("SELECT * FROM preference_template WHERE template_id = %s", (template_id,))
        result = cursor.fetchone()

        if not result:
            return (jsonify({"error": "Preference template not found"}), 404)

        cursor.execute("DELETE FROM preference_template WHERE template_id = %s", (template_id,))
        conn.commit()
        
        return (jsonify({"message": "Preference template deleted successfully", "template_id": template_id}), 200)
    
    except Exception as e:
        conn.rollback() # Rollback the transaction if an error occurs
        return (jsonify({"error": str(e)}), 500)
    
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()