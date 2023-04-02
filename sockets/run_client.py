import logging

from client.client import Client, start_generation

if __name__ == "__main__":

    # file = open("example_to_send.jpg", "rb")
    logging.basicConfig(level=logging.DEBUG)
    client = Client()

    start_generation()

    client.send_image()
