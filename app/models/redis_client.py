import redis
from app.config import Config

def get_redis_client():
    try:
        return redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            db=Config.REDIS_DB,
            decode_responses=True
        )
    except redis.ConnectionError as e:
        print(f"Error de conexión con Redis: {e}")
        raise
