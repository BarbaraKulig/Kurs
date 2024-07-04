# app/avatar.py
import os
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)


class AvatarUploader:
    @staticmethod
    def upload_avatar(image_file):
        result = cloudinary.uploader.upload(image_file)
        return result['secure_url']
