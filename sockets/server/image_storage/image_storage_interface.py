import datetime

from PIL import Image


class ImageStorageInterface:

    def save(self, image, name):
        pass

    def load(self, image_name) -> Image:
        pass

    def load_all(self) -> ([Image], [str]):
        pass

    def load_all_after(self, timestamp: datetime) -> ([Image], [str]):
        pass

    def files_names(self) -> [str]:
        pass
