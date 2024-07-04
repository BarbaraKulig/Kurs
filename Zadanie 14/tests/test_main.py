# tests/test_main.py

import unittest
from app.main import app


class TestMain(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        result = self.app.get('/')
        self.assertEqual(result.data.decode(), 'Hello, World!')


if __name__ == '__main__':
    unittest.main()
