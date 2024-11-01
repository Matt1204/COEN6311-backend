from flask import Blueprint, request
from .controllers.signup_controller import signup_user
from .controllers.auth_controller import auth_user
from .controllers.refresh_token_controller import refresh_access_token
from .controllers.demo_controller import hello_world  # Import the new controller
from .controllers.verify_access_token import verify_access_token
from .controllers.logout_controller import logout_user

my_blueprint = Blueprint("my_blueprint", __name__)


@my_blueprint.route("/signup", methods=["POST"])
def signup():
    data = request.json
    return signup_user(data)


@my_blueprint.route("/auth", methods=["POST"])
def auth():
    data = request.json
    return auth_user(data)


@my_blueprint.route("/refresh", methods=["GET"])
def refresh():
    return refresh_access_token()


@my_blueprint.route("/logout", methods=["GET"])
def logout():
    return logout_user()


@my_blueprint.route("/demo", methods=["GET"])  # New route for demo
@verify_access_token
def demo():
    return hello_world()
