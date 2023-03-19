import logging
from network_manager.network_manager import NetworkManager
from image_storage.image_storage_interface import ImageStorageInterface
from image_storage.HDF5_image_storage import HDF5ImageStorage


class ServerRunner:

    network_manager: NetworkManager
    image_storage: ImageStorageInterface

    def __init__(self):
        self.image_storage = HDF5ImageStorage()
        self.network_manager = NetworkManager(self.image_storage)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server_runner = ServerRunner()
