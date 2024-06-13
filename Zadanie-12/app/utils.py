import re

def validate_email(email):
    # Prosta walidacja e-maila
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True

def validate_password(password):
    # Walidacja hasła
    if len(password) < 6:
        return False
    return True
