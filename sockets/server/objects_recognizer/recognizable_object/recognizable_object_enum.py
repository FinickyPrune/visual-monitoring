import enum
from datetime import datetime

from server.objects_recognizer.recognizable_object.recognizable_object_interface import RecognizableObjectInterface
from server.objects_recognizer.recognizable_object.red_square_object import RedSquareObject


class RecognizableObjectType(enum.Enum):
    RED_SQUARE = 0
    DUCKIEBOT = 1
    QR_CODE = 2

    def create(self, timestamp: datetime, coordinates: [int]) -> RecognizableObjectInterface:
        if self == RecognizableObjectType.RED_SQUARE:
            return RedSquareObject(timestamp=timestamp, coordinates=coordinates)
        if self == RecognizableObjectType.DUCKIEBOT:
            return RecognizableObjectInterface()
        if self == RecognizableObjectType.QR_CODE:
            return RecognizableObjectInterface()
