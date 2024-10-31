from flask import request, jsonify, abort
from functools import wraps
import jwt
import os


def verify_access_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # cookie_rt = request.cookies.get("refreshToken")
        # REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")
        # try:
        #     decoded_rt = jwt.decode(
        #         cookie_rt, REFRESH_TOKEN_SECRET, algorithms=["HS256"]
        #     )
        #     print(decoded_rt)
        # except jwt.ExpiredSignatureError:
        #     # rt is expired
        #     print("RT expire")
        #     return "", 403
        # except jwt.InvalidTokenError:
        #     # rt is invalid
        #     print("RT invalid")
        #     return "", 403

        authHeader = request.headers.get(
            "Authorization", ""
        )  # Get the authorization header
        if not authHeader.startswith("Bearer "):
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
            # abort(401)  # Unauthorized access

        token = authHeader.split(" ")[1]
        try:
            # Verify AT
            decoded = jwt.decode(
                token, os.getenv("ACCESS_TOKEN_SECRET"), algorithms=["HS256"]
            )

        except jwt.ExpiredSignatureError:
            print("verift_access_token(): AT timeout")
            # abort(403)  # Forbidden access - token expired
            return (
                jsonify(
                    {
                        "error": "Unauthorized",
                        "message": "Token is invalid or expired or missed",
                    }
                ),
                401,
            )
        except (jwt.InvalidTokenError, IndexError):
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
            # abort(403)  # Forbidden access - invalid token

        return f(*args, **kwargs)

    return decorated_function
