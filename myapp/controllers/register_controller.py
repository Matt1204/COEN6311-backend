from ..config import get_db_connection
from flask import jsonify
import bcrypt

def register_user(user_data):
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    email = user_data.get('email')
    password = user_data.get('password')
    first_name = user_data.get('first_name', '')
    last_name = user_data.get('last_name', '')

    if not (email and password and first_name and last_name):
        return jsonify({"error": "Missing required fields"}), 400

    cursor = conn.cursor()
    try:
        # Check for existing user
        check_query = "SELECT email FROM user WHERE email = %s"
        cursor.execute(check_query, (email,))
        if cursor.fetchone():
            return jsonify({"error": "Email already in use"}), 409
        
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Insert new user
        query = """
        INSERT INTO user (email, password, first_name, last_name, created_at, updated_at)
        VALUES (%s, %s, %s, %s, NOW(), NOW())
        """
        params = (email, hashed_password, first_name, last_name)  
        cursor.execute(query, params)
        conn.commit()
        return jsonify({"success": f"{email} registered successfully"}), 201
    except Exception as e:
        conn.rollback()  # Rollback in case of any error
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()
