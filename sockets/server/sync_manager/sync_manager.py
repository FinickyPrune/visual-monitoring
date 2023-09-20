import operator

from models.image import ImageDto


class SyncManager:

    @staticmethod
    def sort_images(images: [ImageDto]):
        images.sort(key=lambda image_dto: image_dto.timestamp)
