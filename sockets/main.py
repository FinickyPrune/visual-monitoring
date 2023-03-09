import logging
import server
import client

if __name__ == '__main__':
    file = open("example_to_send.jpg", "rb")
    logging.basicConfig(level=logging.DEBUG)
