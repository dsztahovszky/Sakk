import socket
from typing import Literal


class ChessServer(socket.socket):
    def __init__(self, server_type: Literal["server", "client"], host=..., port=...):
        self.server_type = server_type
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        if self.server_type == "server":
            self.bind((host, port))
            self.conn: socket.socket | None = None
            print(f'Szerver elindult a következő címen: {host}:{port}')

    def wait_for_connection(self):
        self.listen()
        try:
            self.conn, addr = self.accept()
            return addr
        except OSError:
            pass

    def receive(self):
        data = self.conn.recv(1024) if self.server_type == "server" else self.recv(1024)
        if data:
            return data.decode()

    def connect_to_server(self, host, port):
        self.connect((host, port))
        print(f'Kapcsolódás a szerverhez: {host}:{port}')

    def send_message(self, msg):
        if self.server_type == "server":
            self.conn.sendall(msg.encode())
        else:
            self.sendall(msg.encode())

    def close_server(self):
        if isinstance(self.conn, socket.socket):
            self.conn.close()
        self.close()

# def start_server():
#     server = ChessServer('0.0.0.0', 12345)
#     server.wait_for_connection()
#     server.receive()
