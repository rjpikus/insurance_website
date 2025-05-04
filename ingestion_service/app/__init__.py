from flask import Flask
from .logger import setup_logger
from .database import init_db
from .extensions import db
logger = setup_logger()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    # Initialize database (create tables)
    with app.app_context():
        init_db(app)

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app