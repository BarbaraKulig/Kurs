# tests/test_user.py

import unittest
from app.user import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User('testuser', 'test@example.com')

    def test_update_avatar(self):
        self.assertIsNone(self.user.avatar_url)
        self.user.update_avatar('https://example.com/avatar.jpg')
        self.assertEqual(self.user.avatar_url, 'https://example.com/avatar.jpg')


if __name__ == '__main__':
    unittest.main()
