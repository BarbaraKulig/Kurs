# tests/test_avatar.py

import unittest
from app.avatar import AvatarUploader

class TestAvatarUploader(unittest.TestCase):
    def test_upload_avatar(self):
        image_file = 'path/to/avatar.jpg'
        avatar_url = AvatarUploader.upload_avatar(image_file)
        self.assertTrue(avatar_url.startswith('https://res.cloudinary.com/'))

if __name__ == '__main__':
    unittest.main()
