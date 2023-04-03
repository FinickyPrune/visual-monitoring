import logging

from server.server_runner import ServerRunner

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    server = ServerRunner()
