import logging

from models.image import ImageDto
from server.objects_recognizer.recognizable_object.recognizable_object_enum import RecognizableObjectType
from server.objects_recognizer.recognizable_object.recognizable_object_interface import RecognizableObjectInterface


class ObjectRecognizer:

    object_type: RecognizableObjectType
    objects: [RecognizableObjectInterface]

    def __init__(self, object_type: RecognizableObjectType):
        self.object_type = object_type

    def process(self, image_dtos: [ImageDto]):
        for dto in image_dtos:
            self.recognize(dto)

    def recognize(self, image_dto: ImageDto):
        logging.debug("[recognition here]")

        logging.debug("[coordinates here]")
        coordinates = [0, 0, 0]

        self.objects.append(self.object_type.create(image_dto.timestamp, coordinates))



