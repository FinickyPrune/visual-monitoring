import logging
import os
from client.red_square_generator import start_generation
from client.client import Client
from utils.constants import CAMERA_OUTPUT_PATH

if __name__ == "__main__":
    # file = open("example_to_send.jpg", "rb")
    logging.basicConfig(level=logging.DEBUG)
    start_generation()
    client = Client()
