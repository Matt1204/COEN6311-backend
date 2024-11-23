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
from .controllers.preference_controllers.create_preference_controller import (
    create_preference,
)
from .controllers.preference_controllers.get_preference_controller import get_preference
from .controllers.preference_controllers.update_preference_controller import update_pref
from .controllers.request_controllers.get_req_list_controller import get_req_list
from .controllers.request_controllers.get_req_controller import get_req
from .controllers.request_controllers.create_req_controller import create_req
from .controllers.request_controllers.update_req_controller import update_req


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


@my_blueprint.route("/preference/create-preference", methods=["POST"])
@verify_access_token
def create_pref_route():
    pref_data = request.json
    return create_preference(pref_data)


@my_blueprint.route("/preference/get-preference", methods=["GET"])
@verify_access_token
def get_pref_route():
    return get_preference()


@my_blueprint.route("/preference/delete-preference", methods=["DELETE"])
@verify_access_token
def del_pref_route():
    return "delete-pref"


@my_blueprint.route("/preference/update-preference", methods=["PUT"])
@verify_access_token
def update_pref_route():
    pref_data = request.json
    return update_pref(pref_data)


@my_blueprint.route("/request/get-req-list", methods=["GET"])
@verify_access_token
def get_req_list_route():
    return get_req_list()


@my_blueprint.route("/request/get-req", methods=["GET"])
@verify_access_token
def get_req_route():
    return get_req()


@my_blueprint.route("/request/create-req", methods=["POST"])
@verify_access_token
def create_req_route():
    data = request.json
    return create_req(data)


@my_blueprint.route("/request/update-req", methods=["PUT"])
@verify_access_token
def update_req_route():
    data = request.json
    return update_req(data)


@my_blueprint.route("/demo", methods=["GET"])  # New route for demo
@verify_access_token
def demo():
    return hello_world()
