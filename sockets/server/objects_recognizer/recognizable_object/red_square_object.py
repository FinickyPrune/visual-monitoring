from datetime import datetime

from server.objects_recognizer.recognizable_object.recognizable_object_interface import RecognizableObjectInterface


class RedSquareObject(RecognizableObjectInterface):

    def __init__(self, timestamp: datetime, coordinates: [float]):
        self.timestamp = timestamp
        self.coordinates = coordinates
