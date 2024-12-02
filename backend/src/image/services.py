import cloudinary
import cloudinary.api

from src.config import settings

cloudinary.config(
    cloud_name=settings.cloudinary.CLOUD_NAME,
    api_key=settings.cloudinary.CLOUD_API_KEY,
    api_secret=settings.cloudinary.CLOUD_API_SECRET,
    secure=True,
)


def delete_images(public_ids: list[str]) -> None:
    cloudinary.api.delete_resources(public_ids)
