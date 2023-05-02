from datetime import datetime
from typing import List


class RecognizableObjectInterface:
    timestamp: datetime
    coordinates: List[float]
