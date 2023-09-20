import concurrent.futures
import logging

from server.estimator.estimator import Estimator
from server.network_manager.network_manager import NetworkManager
from server.image_storage.image_storage_interface import ImageStorageInterface
from server.image_storage.HDF5_image_storage import HDF5ImageStorage
from server.image_buffer.image_buffer import ImageBuffer
from server.objects_recognizer.objects_recognizer import ObjectRecognizer
from server.objects_recognizer.recognizable_object.recognizable_object_enum import RecognizableObjectType
from server.result_visualizer.result_visualizer import ResultVisualizer


class ServerRunner:
    network_manager: NetworkManager
    image_storage: ImageStorageInterface
    image_buffer: ImageBuffer
    objects_recognizer: ObjectRecognizer
    estimator: Estimator
    result_visualizer: ResultVisualizer

    def run_network_manager(self):
        self.network_manager = NetworkManager(self.image_storage)

    def run_image_buffer(self):
        self.result_visualizer = ResultVisualizer()
        self.estimator = Estimator(observer=self.result_visualizer)
        self.objects_recognizer = ObjectRecognizer(object_type=RecognizableObjectType.RED_SQUARE,
                                                   observer=self.estimator)
        self.image_buffer = ImageBuffer(self.image_storage, self.objects_recognizer)

    def __init__(self):
        self.image_storage = HDF5ImageStorage()

        pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)

        pool.submit(self.run_network_manager)
        pool.submit(self.run_image_buffer)


        # wait for all tasks to complete
        # pool.shutdown(wait=True)
