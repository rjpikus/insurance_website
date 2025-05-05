import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask configuration
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# Redis configuration
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# RQ configuration
RQ_QUEUE_NAME = os.getenv('RQ_QUEUE_NAME', 'batch_processing')

# Ray configuration
RAY_ADDRESS = os.getenv('RAY_ADDRESS', None)  # None means start a local Ray instance
RAY_NUM_CPUS = int(os.getenv('RAY_NUM_CPUS', 2))

# Application settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
TIMEOUT = int(os.getenv('TIMEOUT', 3600))  # Default timeout for jobs in seconds
