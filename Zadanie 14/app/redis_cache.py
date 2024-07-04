# app/redis_cache.py

import redis
import os

redis_client = redis.StrictRedis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    password=os.getenv('REDIS_PASSWORD'),
    decode_responses=True
)


class RedisCache:
    @staticmethod
    def cache_user_data(user_id, data):
        redis_client.set(f'user:{user_id}', data)

    @staticmethod
    def get_cached_user_data(user_id):
        return redis_client.get(f'user:{user_id}')
