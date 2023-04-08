from math import ceil, floor
import os
import pickle
import socket
import logging
from time import sleep
from typing import Generator, Tuple

from PIL import Image
from datetime import datetime

import numpy as np

from models.image import ImageDto
from utils.constants import HOST, PORT, CAMERA_OUTPUT_PATH, BYTE_CHUNK


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
                    pixels[
                        y, min(int(current_x + x), self.__image_size[0] - 1)
                    ] = tuple(RED)
                pixels[
                    y, min(int(current_x + self.__w - 1), self.__image_size[0] - 1)
                ] = tuple(np.array(RED * last_density, dtype=np.uint8))

            yield im


class Client:
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.socket.connect((HOST, PORT))
        try:
            self.process_directory()
        except KeyboardInterrupt:
            logging.info("Caught keyboard interrupt, exiting")
        finally:
            self.socket.close()

    def process_directory(self):
        files = os.listdir(CAMERA_OUTPUT_PATH)
        iterator = 0
        while iterator != len(files):
            filename = files[iterator]
            iterator += 1
            if filename[-3:] != "png":
                continue
            path = os.path.join(CAMERA_OUTPUT_PATH, filename)
            self.send_image(path)

            files = os.listdir(
                CAMERA_OUTPUT_PATH
            )  # In case new images appear in directory while old being sent

    def send_image(self, path, square_debug=False):
        image = Image.open(path)

        dto_dump = pickle.dumps(ImageDto(datetime.utcnow(), image))
        dto_length_bytes = len(dto_dump).to_bytes(4, "big")

        self.socket.send(dto_length_bytes)

        for i in range(0, len(dto_dump), BYTE_CHUNK):
            self.socket.send(dto_dump[i : i + BYTE_CHUNK])

        logging.info(f"{path} sent.")
