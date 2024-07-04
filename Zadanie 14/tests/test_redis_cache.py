# tests/test_redis_cache.py

import unittest
from app.redis_cache import RedisCache


class TestRedisCache(unittest.TestCase):
    def setUp(self):
        self.user_id = 123
        self.data = '{"username": "testuser"}'

    def test_cache_user_data(self):
        RedisCache.cache_user_data(self.user_id, self.data)
        cached_data = RedisCache.get_cached_user_data(self.user_id)
        self.assertEqual(cached_data, self.data)


if __name__ == '__main__':
    unittest.main()
