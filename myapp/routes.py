from flask import Blueprint, request
from .controllers.demo_controller import hello_world  # Import the new controller
from .controllers.auth_controllers.signup_controller import signup_user
from .controllers.auth_controllers.auth_controller import auth_user
from .controllers.auth_controllers.refresh_token_controller import refresh_access_token
from .controllers.auth_controllers.verify_access_token import verify_access_token
from .controllers.auth_controllers.logout_controller import logout_user
from .controllers.user_controllers.get_user_controller import get_user
from .controllers.user_controllers.update_user_controller import update_user
from .controllers.hospital_controllers.get_all_hospitals import get_all_hospitals

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


@my_blueprint.route("/get-all-hospitals", methods=["GET"])
def get_all_hospital_route():
    return get_all_hospitals()


@my_blueprint.route("/get-user", methods=["GET"])
@verify_access_token
def get_user_route():
    return get_user()


@my_blueprint.route("/update-user", methods=["PUT"])
@verify_access_token
def update_user_route():
    data = request.json
    return update_user(data)


@my_blueprint.route("/demo", methods=["GET"])  # New route for demo
@verify_access_token
def demo():
    return hello_world()
