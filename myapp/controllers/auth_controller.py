from ..config import get_db_connection
from flask import jsonify, make_response, request
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
import os
import json


def auth_user(user_data):
    # Check if email and password are provided
    email = user_data.get("email")
    password = user_data.get("password")
    if not email or not password:
        return (
            jsonify(
                {
                    "error": "client-side issue",
                    "message": "Please provide complete form",
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
        # find email
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        foundUser = cursor.fetchone()
        if foundUser is None:
            return (
                jsonify(
                    {
                        "error": "account not found",
                        "message": "Incorrect Email or Password",
                    }
                ),
                404,
            )
        # Verify the password
        hashed_password = foundUser["password"]
        match = bcrypt.checkpw(
            password.encode("utf-8"), hashed_password.encode("utf-8")
        )

        # good user
        if match:
            ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
            REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")
            # Generate Access token
            new_access_token = jwt.encode(
                {
                    "UserInfo": {
                        "email": foundUser["email"],
                        "role": foundUser["role"],
                        # "first_name": foundUser["first_name"],
                        # "last_name": foundUser["last_name"],
                    },
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=10),
                },
                ACCESS_TOKEN_SECRET,
                algorithm="HS256",
            )
            # Generate refresh token
            new_refresh_token = jwt.encode(
                {
                    "email": foundUser["email"],
                    "exp": datetime.now(timezone.utc) + timedelta(hours=3),
                },
                REFRESH_TOKEN_SECRET,
                algorithm="HS256",
            )

            response_data = {
                "email": foundUser["email"],
                "first_name": foundUser["first_name"],
                "last_name": foundUser["last_name"],
                "access_token": new_access_token,
                "role": foundUser["role"],
            }
            response = make_response(jsonify(response_data), 200)

            # Parse the refresh token list from the db
            db_rt_list = (
                json.loads(foundUser["refresh_token"])
                if foundUser["refresh_token"]
                else []
            )
            # print(f"! Old database refresh_token({len(db_rt_list)}): {db_rt_list}")

            new_rt_list = []
            cookie_rt = request.cookies.get("refreshToken")
            # prepare data for updating database refersh token
            # check if cookie.rt exist in reqeust
            if cookie_rt:
                # filter out the cookie.rt from database
                new_rt_list = [rt for rt in db_rt_list if rt != cookie_rt]
                # response.set_cookie(
                #     "refreshToken", "", expires=0
                # )  # remove rt from cookie
                response.delete_cookie("refreshToken")
                print(f"! remove RT from db")
            else:
                print("! no cookie.rt, no change to database")
                new_rt_list = db_rt_list

            # update database with new refreh token list
            new_rt_list.append(new_refresh_token)
            print(f"! new database refresh_token({len(db_rt_list)})")
            cursor.execute(
                "UPDATE user SET refresh_token = %s WHERE email = %s",
                (json.dumps(new_rt_list), email),
            )
            conn.commit()

            response.set_cookie(
                "refreshToken",
                new_refresh_token,
                httponly=True,
                # secure=False,
                # samesite="None",
                max_age=3600,
                secure=True,
                samesite="None",  # Allow cross-site cookie sharing
            )

            print(f"! new RT")
            print(f"! new AT")
            return response

        else:
            return (
                jsonify(
                    {
                        "error": "account not found",
                        "message": "Incorrect Email or Password",
                    }
                ),
                403,
            )

    except Exception as e:
        # Handle general exceptions
        print(e)
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()
