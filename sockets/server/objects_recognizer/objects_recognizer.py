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
from cv2 import aruco

class ObjectRecognizer(Observer, Subject, ABC):
    object_type: RecognizableObjectType
    objects: List[RecognizableObjectInterface] = []

    observers: List[Observer] = []

    last_index: int = 0

    # aruco init
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_1000)
    arucoParams = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, arucoParams)

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

        if self.object_type == RecognizableObjectType.RED_SQUARE:
            img = np.array(image_dto.image)

            blue_thresh = cv2.inRange(img, (250, 0, 0), (255, 0, 0))
            black_thresh = cv2.inRange(img, (0, 0, 0), (5, 5, 5))

            blue_square_coordinates = np.where(blue_thresh == 255)
            black_square_coordinates = np.where(black_thresh == 255)

            robot_coords = np.mean(blue_square_coordinates, axis=1)
            robot_coords /= np.shape(img)[:2]
            robot_facing = np.mean(black_square_coordinates, axis=1) - robot_coords
            robot_facing /= norm(robot_facing)

            recognized_object = self.object_type.create(
                image_dto.timestamp, robot_coords, robot_facing
            )
            self.objects.append(recognized_object)

        elif self.object_type == RecognizableObjectType.QR_CODE:
            img = cv2.cvtColor(np.array(image_dto.image), cv2.COLOR_RGB2GRAY)
            corners, ids, rejectedImgPoints = self.detector.detectMarkers(img)

            if len(corners) == 0:
                # markers_data[img_idx]["corners"] = []
                # markers_data[img_idx]["ids"] = []
                # markers_data[img_idx]["center"] = []
                return
            # markers_data[img_idx]["corners"] = corners
            # markers_data[img_idx]["ids"] = ids
            centers = []
            for c in corners:
                m = cv2.moments(c)
                cx = m['m10'] / (m['m00'] + 1e-5)
                cy = m['m01'] / (m['m00'] + 1e-5)
                robot_coords = (cx / np.shape(img)[1], cy / np.shape(img)[1])
            # markers_data[img_idx]["centers"] = centers

            # recognized_object = self.object_type.create(
            #     image_dto.timestamp, robot_coords, robot_facing
            # )
            # self.objects.append(recognized_object)

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
