import logging

from server.server_runner import ServerRunner

if __name__ == "__main__":

    # file = open("example_to_send.jpg", "rb")
    logging.basicConfig(level=logging.DEBUG)
    server = ServerRunner()
