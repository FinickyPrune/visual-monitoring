from PIL import Image

class ImageStorageInterface:

    def save(self, image, name):
        pass

    def load(self, image_name) -> Image:
        pass

    def files_names(self) -> [str]:
        pass
