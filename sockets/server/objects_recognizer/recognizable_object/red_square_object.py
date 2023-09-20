from datetime import datetime
from typing import List

from dataclasses import dataclass

from server.objects_recognizer.recognizable_object.recognizable_object_interface import (
    RecognizableObjectInterface,
)


@dataclass
class RedSquareObject(RecognizableObjectInterface):
    """
    :param timestamp:   - Time where shot was recognised.
    :param coordinates: - (y, x) where robot is standing.
    :param towards:     - (y, x) way robot is looking rn.
    """

    timestamp: datetime
    coordinates: List[float]
    towards: List[float]
