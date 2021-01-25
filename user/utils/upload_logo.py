import cloudinary
from rest_framework import serializers


def upload_image_to_cloudinary(image):
    limit_mb = 5
    file_size = image.size
    if file_size > limit_mb * 1024 * 1024:
        raise serializers.ValidationError(
            "Max size of file is %s MB" % limit_mb)

    cloudinary_file = cloudinary.uploader.upload(
        image, resource_type="raw")
    return cloudinary_file['secure_url']
