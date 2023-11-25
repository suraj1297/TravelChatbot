from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import the API views here
    from .api.views import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
