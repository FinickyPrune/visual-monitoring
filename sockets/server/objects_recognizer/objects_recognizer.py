import logging
from abc import ABC
from typing import List

from models.image import ImageDto
from server.image_buffer.image_buffer import ImageBuffer
from server.objects_recognizer.recognizable_object.recognizable_object_enum import (
    RecognizableObjectType,
)
from server.objects_recognizer.recognizable_object.recognizable_object_interface import (
    RecognizableObjectInterface,
)
from server.observer_interface.observer import Observer, Subject
from utils.constants import BUFFER_CHUNK

import cv2
import numpy as np
from numpy.linalg import norm


class ObjectRecognizer(Observer, Subject, ABC):
    object_type: RecognizableObjectType
    objects: List[RecognizableObjectInterface] = []

    observers: List[Observer] = []

    last_index: int = 0

    def __init__(self, object_type: RecognizableObjectType, observer):
        self.object_type = object_type
        self.observers.append(observer)

    def process(self, image_dtos: List[ImageDto]):
        self.objects = []
        for dto in image_dtos:
            self.recognize(dto)
        self.notify()

    def recognize(self, image_dto: ImageDto):
        # logging.debug(f"recognized {image_dto.timestamp}")

        img = np.array(image_dto.image)

        blue_thresh = cv2.inRange(img, (250, 0, 0), (255, 0, 0))
        black_thresh = cv2.inRange(img, (0, 0, 0), (5, 5, 5))

        blue_square_coordinates = np.where(blue_thresh == 255)
        black_square_coordinates = np.where(black_thresh == 255)

        robot_coords = np.mean(blue_square_coordinates, axis=1)
        robot_facing = np.mean(black_square_coordinates, axis=1) - robot_coords
        robot_facing /= norm(robot_facing)

        recognized_object = self.object_type.create(
            image_dto.timestamp, robot_coords, robot_facing
        )
        self.objects.append(recognized_object)

    def update(self, subject: ImageBuffer) -> None:
        logging.debug("Recognizer got dtos")
        image_dtos = subject.image_dtos
        index = self.last_index

        while index != (len(image_dtos) - BUFFER_CHUNK + 1):
            logging.debug(f"----------------------- {index} -----------------------")
            chunk = image_dtos[index : index + BUFFER_CHUNK]
            self.process(chunk)
            index += 1
        self.last_index = index

    def notify(self) -> None:
        for observer in self.observers:
            observer.update(self)
