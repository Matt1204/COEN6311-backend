from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
import os

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins="http://localhost:5173")

    # Import blueprints
    from myapp.routes import my_blueprint
    app.register_blueprint(my_blueprint)
    # print("FLASK_ENV:", os.getenv('FLASK_ENV'))  # Add this line to debug

    return app

if __name__ == "__main__":
    app = create_app()
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.run()

# flask --app app.py --debug run
