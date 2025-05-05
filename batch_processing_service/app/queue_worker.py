import os
import sys
import time
import redis
from rq import Worker, Queue, Connection
import logging
from .config import REDIS_URL, RQ_QUEUE_NAME, LOG_LEVEL

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_worker():
    """
    Start an RQ worker to process jobs from the queue
    
    This function connects to Redis and starts a worker process
    that will listen for and execute jobs from the specified queue.
    """
    try:
        # Connect to Redis
        redis_conn = redis.from_url(REDIS_URL)
        logger.info(f"Connected to Redis at {REDIS_URL}")
        
        # Get worker ID or generate one
        worker_id = os.getenv('WORKER_ID', f'worker-{os.getpid()}')
        
        # Start worker
        logger.info(f"Starting worker {worker_id} for queue {RQ_QUEUE_NAME}")
        
        with Connection(redis_conn):
            queue = Queue(RQ_QUEUE_NAME)
            worker = Worker([queue], name=worker_id)
            worker.work(with_scheduler=True)
    
    except Exception as e:
        logger.error(f"Worker error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    run_worker()
