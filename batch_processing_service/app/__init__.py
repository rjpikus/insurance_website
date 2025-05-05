# This file makes the app directory a Python package
from flask import Flask
from rq import Queue
from redis import Redis
import logging
from .config import REDIS_URL, LOG_LEVEL, RQ_QUEUE_NAME

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Redis connection
redis_conn = Redis.from_url(REDIS_URL)

# Initialize RQ queue
task_queue = Queue(RQ_QUEUE_NAME, connection=redis_conn)

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Import and register blueprints/routes
    from .main import bp as main_bp
    app.register_blueprint(main_bp)
    
    @app.route('/health')
    def health_check():
        """Simple health check endpoint"""
        return {'status': 'healthy'}, 200
    
    return app
