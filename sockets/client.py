import socket
import logging

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


class Client:

    def __init__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall("Hello, world")
            data = s.recv(1024)

        logging.info(f"Received {data!r}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    client = Client()
