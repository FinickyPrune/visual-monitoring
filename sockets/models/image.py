from dataclasses import dataclass
from datetime import datetime
from PIL import Image


@dataclass
class ImageDto:
    timestamp: datetime
    image: Image

@dataclass
class ImageRawData:
    image_bytes: [] = None
    size: int = 0


