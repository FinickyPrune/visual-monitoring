import logging
import pickle
import socket
import selectors
import types
from image import ImageRawData

sel = selectors.DefaultSelector()

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


class Server:
    files = dict()

    def __init__(self):
        host, port = HOST, PORT
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((host, port))
        lsock.listen()

        logging.info(f"Listening on {(host, port)}")
        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ, data=None)

        try:
            while True:
                events = sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.server_connection(key, mask)
        except KeyboardInterrupt:
            logging.info("Caught keyboard interrupt, exiting")
        finally:
            sel.close()

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        logging.info(f"Accepted connection from {addr}")
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ
        sel.register(conn, events, data=data)
        self.files[addr] = ImageRawData()

    def server_connection(self, key, mask):
        sock = key.fileobj
        addr = sel.get_key(sock).data.addr
        if mask & selectors.EVENT_READ:
            if self.files[addr].image_bytes is None:
                image_length_bytes = sock.recv(4)
                if image_length_bytes:
                    self.files[addr] = ImageRawData([], int.from_bytes(image_length_bytes, 'big'))
                    logging.debug(int.from_bytes(image_length_bytes, 'big'))
                else:
                    logging.info(f"Closing connection to {sel.get_key(sock).data.addr}")
                    sel.unregister(sock)
                    sock.close()

            else:
                image = self.files[addr]
                recv_data = sock.recv(min(4096, image.size))
                if recv_data is None:
                    return
                image.image_bytes.append(recv_data)
                logging.debug(image.size)
                image.size -= len(recv_data)
                if image.size == 0:
                    image_dto = pickle.loads(b''.join(image.image_bytes))
                    image_dto.image.save(str(addr) + "_" + image_dto.timestamp + '.jpg')
                    self.files[addr] = ImageRawData()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server = Server()
