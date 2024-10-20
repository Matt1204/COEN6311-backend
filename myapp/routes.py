from flask import Blueprint, request
from .controllers.register_controller import register_user
from .controllers.auth_controller import auth_user

from .controllers.demo_controller import hello_world  # Import the new controller

my_blueprint = Blueprint('my_blueprint', __name__)

@my_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    return register_user(data)

@my_blueprint.route('/auth', methods=['POST'])
def auth():
    data = request.json
    return auth_user(data)

@my_blueprint.route('/demo', methods=['GET'])  # New route for demo
def demo():
    return hello_world()