# if access token has problem, status code must be 401

from flask import request, jsonify, abort
from functools import wraps
import jwt
import os


def verify_access_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # parse access token
        authHeader = request.headers.get("Authorization", "")
        if authHeader is None or not authHeader.startswith("Bearer "):
            print("verift_access_token(): no Bearer token detected!!!")
            return (
                jsonify(
                    {
                        "error": "Unauthorized",
                        "message": "Token is invalid or expired or missed",
                    }
                ),
                401,
            )

        # verify access token
        access_token = authHeader.split(" ")[1]
        print(f"verift_access_token() get AT:" + access_token)
        try:
            jwt.decode(
                access_token, os.getenv("ACCESS_TOKEN_SECRET"), algorithms=["HS256"]
            )

        except jwt.ExpiredSignatureError:
            print("verift_access_token(): AT timeout")
            return (
                jsonify(
                    {
                        "error": "Unauthorized",
                        "message": "Token is invalid or expired or missed",
                    }
                ),
                401,
            )
        except jwt.InvalidTokenError:
            print("verift_access_token(): AT invalid")
            return (
                jsonify(
                    {
                        "error": "Unauthorized",
                        "message": "Token is invalid or expired or missed",
                    }
                ),
                401,
            )

        return f(*args, **kwargs)

    return decorated_function
