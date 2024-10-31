from flask import jsonify, make_response, request
import jwt
from datetime import datetime, timedelta, timezone
import os
from ..config import get_db_connection
import json


def refresh_access_token():
    cookie_rt = request.cookies.get("refreshToken")
    print(f"! /refersh get cookie_rt: {cookie_rt}")
    if not cookie_rt:
        print("no RT in cookie")
        return (
            jsonify(
                {
                    "error": "Unauthorized",
                    "message": "Refresh token is missing",
                }
            ),
            403,
        )

    # verify cookie.rt
    REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")
    try:
        decoded = jwt.decode(cookie_rt, REFRESH_TOKEN_SECRET, algorithms=["HS256"])
        print(f"! /refersh cookie_rt: {decoded}")
    except jwt.ExpiredSignatureError:
        # rt is expired
        print("! /REFRESH RT expire")
        # return "", 403  # OK
        return (
            jsonify(
                {
                    "error": "Unauthorized",
                    "message": "Refresh Token is expired",
                }
            ),
            403,
        )
    except jwt.InvalidTokenError:
        # rt is invalid
        print("! /REFRESH RT invalid")
        # return "", 403
        return (
            jsonify(
                {
                    "error": "Unauthorized",
                    "message": "Refresh Token is invalid",
                }
            ),
            403,
        )

    try:
        conn = get_db_connection()
        if conn is None:
            # return jsonify({"error": "Database connection failed"}), 500
            return (
                jsonify(
                    {
                        "error": "internal error",
                        "message": "Database connection failed",
                    }
                ),
                500,
            )
        # return "", 403
        cursor = conn.cursor(dictionary=True)

        # geting cookie.email
        cookie_email = decoded.get("email")
        print(f"! /refresh cookie_email: {cookie_email}")
        if not cookie_email:
            # return jsonify({'error': 'Invalid token data'}), 401
            print("! /REFRESH No email in cookie RT")
            # return "", 204
            return (
                jsonify(
                    {
                        "error": "Unauthorized",
                        "message": "no emial in RT",
                    }
                ),
                403,
            )

        # find user from db using cookie.email
        cursor.execute("SELECT * FROM user WHERE email = %s", (cookie_email,))
        foundUser = cursor.fetchone()

        if foundUser is None:
            print("! /REFRESH Can't find user using cookie.email")
            # return "", 204
            return (
                jsonify(
                    {
                        "error": "Unauthorized",
                        "message": "RT emial invalid",
                    }
                ),
                403,
            )
        print(f"! /refresh foundUser: {foundUser['email']}")
        # parse db refresh_token list
        db_refresh_tokens = (
            json.loads(foundUser["refresh_token"]) if foundUser["refresh_token"] else []
        )

        # Check if the cookie.rt is in db
        if cookie_rt not in db_refresh_tokens:
            print("! /REFRESH cookie RT is NOT in database")
            # return jsonify({"error": "cookie_rt not in database"}), 401
            return (
                jsonify(
                    {
                        "error": "Unauthorized",
                        "message": "fake RT",
                    }
                ),
                403,
            )

        # Generate a new access token
        ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
        new_access_token = jwt.encode(
            {
                "UserInfo": {
                    "email": foundUser["email"],
                    # 'roles': foundUser['roles']
                    "first_name": foundUser["first_name"],
                    "last_name": foundUser["last_name"],
                },
                "exp": datetime.now(timezone.utc) + timedelta(seconds=10),
            },
            ACCESS_TOKEN_SECRET,
            algorithm="HS256",
        )
        print(f"! /REFRESH new AT")
        response_data = {
            "email": foundUser["email"],
            "first_name": foundUser["first_name"],
            "last_name": foundUser["last_name"],
            "role": foundUser["role"],
            "access_token": new_access_token,
        }

        return jsonify(response_data), 200

    except Exception as e:
        print("! /REFRESH catch general error")
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
