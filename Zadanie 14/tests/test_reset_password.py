# tests/test_reset_password.py

import unittest
from app.reset_password import PasswordResetter

class TestPasswordResetter(unittest.TestCase):
    def test_reset_password(self):
        email = 'test@example.com'
        result = PasswordResetter.reset_password(email)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
