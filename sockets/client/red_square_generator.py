import logging
from math import ceil, floor
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
        self.__h, self.__w = square_size

    def generate(self) -> Generator[None, None, Image.Image]:
        shift = self.__image_size[1] / self.__target_count
        RED = np.array((255, 0, 0), dtype=np.uint8)

        for i in range(self.__target_count):
            sleep(0.2)

            im = Image.new("RGB", self.__image_size, "black")
            pixels = im.load()
            i_shifted = i * shift
            current_x, next_x = floor(i_shifted), ceil(i_shifted)
            first_density = i_shifted - current_x
            last_density = next_x - i_shifted

            for y in range(self.__h):
                pixels[y, int(current_x)] = tuple(
                    np.array(RED * first_density, dtype=np.uint8)
                )
                for x in range(1, self.__w - 1):
                    pixels[y, int(current_x + x)] = tuple(RED)
                pixels[y, int(current_x + self.__w - 1)] = tuple(
                    np.array(RED * last_density, dtype=np.uint8)
                )

            yield im


def start_generation():
    rsg = RedSquareGenerator()
    i = 0
    for image in rsg.generate():
        image.save(f"{CAMERA_OUTPUT_PATH}image_{i}.png")
        i += 1
    logging.info("Finished generating.")