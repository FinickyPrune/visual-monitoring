import concurrent.futures
import logging
from server.network_manager.network_manager import NetworkManager
from server.image_storage.image_storage_interface import ImageStorageInterface
from server.image_storage.HDF5_image_storage import HDF5ImageStorage
from server.image_buffer.image_buffer import ImageBuffer


class ServerRunner:
    network_manager: NetworkManager
    image_storage: ImageStorageInterface
    image_buffer: ImageBuffer

    def run_network_manager(self):
        self.network_manager = NetworkManager(self.image_storage)

    def run_image_buffer(self):
        self.image_buffer = ImageBuffer(self.image_storage)

    def __init__(self):
        self.image_storage = HDF5ImageStorage()

        pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)

        pool.submit(self.run_image_buffer)
        pool.submit(self.run_network_manager)

        # wait for all tasks to complete
        pool.shutdown(wait=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    server_runner = ServerRunner()
