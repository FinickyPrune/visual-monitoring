from dataclasses import dataclass
from typing import BinaryIO
from PIL import Image


@dataclass
class ImageDto:
    timestamp: str
    image: Image


@dataclass
class ImageRawData:
    image_bytes: [] = None
    size: int = 0


