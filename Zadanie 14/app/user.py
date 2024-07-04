# app/user.py

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.avatar_url = None

    def update_avatar(self, avatar_url):
        self.avatar_url = avatar_url
