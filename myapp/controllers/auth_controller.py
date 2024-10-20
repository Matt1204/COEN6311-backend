from ..config import get_db_connection
from flask import jsonify
import bcrypt

def auth_user(user_data):
    # Check if email and password are provided
    email = user_data.get('email')
    password = user_data.get('password')
    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)  # Ensure that the cursor returns dictionary-like objects

    try:
        # Check if the user exists
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user is None:
            return jsonify({'error': 'User not found'}), 404

        # Verify the password
        hashed_password = user['password']
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return jsonify({
                'message': 'Success', 
                'body': {
                    'email': user['email'],
                    'firstName': user['first_name'],
                    'lastName': user['last_name']
                }
            }), 200
        else:
            return jsonify({'error': 'Invalid password'}), 401

    except Exception as e:
        # Handle general exceptions
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()
