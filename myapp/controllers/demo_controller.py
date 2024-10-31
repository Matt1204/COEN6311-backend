from flask import jsonify
from datetime import datetime


def hello_world():
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    return jsonify({"message": current_time}), 200
