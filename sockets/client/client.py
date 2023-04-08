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
