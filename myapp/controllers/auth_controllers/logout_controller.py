from flask import jsonify, make_response, request
from ...config import get_db_connection
import jwt
import os
import json


def logout_user():
    cookie_rt = request.cookies.get("refreshToken")
    response = make_response(jsonify({"message": "Log out successful"}), 200)

    if not cookie_rt:
        response.delete_cookie("refreshToken")
        return response

    try:
        REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")
        decoded = jwt.decode(cookie_rt, REFRESH_TOKEN_SECRET, algorithms=["HS256"])
        cookie_email = decoded.get("email")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if cookie_email:
            cursor.execute(
                "SELECT refresh_token FROM user WHERE email = %s", (cookie_email,)
            )
            foundUser = cursor.fetchone()
            if foundUser and foundUser["refresh_token"]:
                # remove cookie rt from db
                db_rt_list = json.loads(foundUser["refresh_token"])
                new_rt_list = [rt for rt in db_rt_list if rt != cookie_rt]
                cursor.execute(
                    "UPDATE user SET refresh_token = %s WHERE email = %s",
                    (json.dumps(new_rt_list), cookie_email),
                )
                conn.commit()

        response.delete_cookie("refreshToken")
        return response
    except jwt.ExpiredSignatureError:
        print("/logout, RT expired, log out")
        response.delete_cookie("refreshToken")
        return response
    except (jwt.InvalidTokenError, Exception) as e:
        print("/logout, erro caught, log out")
        response.delete_cookie("refreshToken")
        return response
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
