from dataclasses import dataclass
from PIL import Image


@dataclass
class ImageDto:
    timestamp: str
    image: Image


@dataclass
class ImageRawData:
    image_bytes: [] = None
    size: int = 0


