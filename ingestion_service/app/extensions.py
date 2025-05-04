import redis
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



redis_client = redis.Redis.from_url(os.environ.get("redis://default:cVLaIDzXOuqYtLXvOcyVdHaCZuFAmGHK@redis.railway.internal:6379", "redis://localhost:6379"))
