# tests/test_email_verification.py

import unittest
from app.email_verification import EmailVerifier

class TestEmailVerifier(unittest.TestCase):
    def test_verify_email(self):
        valid_email = 'test@example.com'
        result = EmailVerifier.verify_email(valid_email)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
