import logging
from time import sleep
from typing import Generator
from typing import Tuple
import numpy as np
from PIL import Image

from utils.constants import CAMERA_OUTPUT_PATH


class RedSquareGenerator:
    def __init__(
        self,
        image_size: Tuple[int, int] = (100, 100),
        square_count: int = 17,
        square_size: Tuple[int, int] = (11, 11),
    ):
        self.__image_size: int = image_size
        self.__target_count: int = square_count
        self.__sq_h, self.__sq_w = square_size

    def generate(self) -> Generator[None, None, Image.Image]:
        RED = np.array((255, 0, 0), dtype=np.uint8)
        BLACK = np.array((0, 0, 0), dtype=np.uint8)
        START_POSITION = (0, 0)

        y_s, x_s = START_POSITION

        for i in range(self.__target_count):
            im = Image.new("RGB", self.__image_size, "white")
            pixels = im.load()

            for y in range(self.__sq_h):
                for x in range(self.__sq_w - 1):
                    pixels[y_s + y, x_s + x + i] = tuple(np.array(RED, dtype=np.uint8))
                pixels[y_s + y, x_s + x + 1 + i] = tuple(
                    np.array(BLACK, dtype=np.uint8)
                )

            yield im

            sleep(1)


def start_generation():
    rsg = RedSquareGenerator()
    i = 0
    for image in rsg.generate():
        image.save(f"{CAMERA_OUTPUT_PATH}image_{i}.png")
        i += 1
    logging.info("Finished generating.")
