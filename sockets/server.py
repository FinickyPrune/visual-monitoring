import logging
import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


class Server:

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
                        self.service_connection(key, mask)
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            sel.close()

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        logging.info(f"Accepted connection from {addr}")
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb += recv_data
            else:
                logging.info(f"Closing connection to {data.addr}")
                sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                logging.info(f"Echoing {data.outb!r} to {data.addr}")
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server = Server()
