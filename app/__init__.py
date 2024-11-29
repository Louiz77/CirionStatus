from flask import Flask
from app.routes import bp as backup_bp
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('app.config.Config')
    app.register_blueprint(backup_bp)
    return app
