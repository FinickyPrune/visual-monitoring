import logging
from abc import ABC
from typing import List

from models.image import ImageDto
from server.image_buffer.image_buffer import ImageBuffer
from server.objects_recognizer.recognizable_object.recognizable_object_enum import RecognizableObjectType
from server.objects_recognizer.recognizable_object.recognizable_object_interface import RecognizableObjectInterface
from server.observer_interface.observer import Observer, Subject
from utils.constants import BUFFER_CHUNK


class ObjectRecognizer(Observer, Subject, ABC):

    object_type: RecognizableObjectType
    objects: [RecognizableObjectInterface] = []

    observers: List[Observer] = []

    last_index: int = 0

    def __init__(self, object_type: RecognizableObjectType, observer):
        self.object_type = object_type
        self.observers.append(observer)

    def process(self, image_dtos: [ImageDto]):
        self.objects = []
        for dto in image_dtos:
            self.recognize(dto)
        self.notify()

    def recognize(self, image_dto: ImageDto):
        # logging.debug(f"recognized {image_dto.timestamp}")

        coordinates = [0, 0, 0]
        recognized_object = self.object_type.create(image_dto.timestamp, coordinates)
        self.objects.append(recognized_object)

    def update(self, subject: ImageBuffer) -> None:
        logging.debug("Recognizer got dtos")
        image_dtos = subject.image_dtos
        index = self.last_index

        while index != (len(image_dtos) - BUFFER_CHUNK + 1):
            logging.debug(f"----------------------- {index} -----------------------")
            chunk = image_dtos[index:index + BUFFER_CHUNK]
            self.process(chunk)
            index += 1
        self.last_index = index

    def notify(self) -> None:
        for observer in self.observers:
            observer.update(self)




