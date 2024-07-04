# app/email_verification.py

import re


class EmailVerifier:
    @staticmethod
    def verify_email(email):
        """
        Sprawdza poprawność formatu adresu e-mail.

        Args:
            email (str): Adres e-mail do zweryfikowania.

        Returns:
            bool: True, jeśli adres e-mail jest poprawny; False w przeciwnym razie.
        """
        # Proste sprawdzenie formatu adresu e-mail
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False

