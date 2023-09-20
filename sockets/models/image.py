from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from PIL.Image import Image


@dataclass
class ImageDto:
    timestamp: datetime
    image: Image


@dataclass
class ImageRawData:
    image_bytes: Optional[bytes] = None
    size: int = 0
