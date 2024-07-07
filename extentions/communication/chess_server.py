import socket
from typing import Literal


class ChessServer(socket.socket):
    def __init__(self, server_type: Literal["server", "client"], host=..., port=...):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        if server_type == "server":
            self.bind((host, port))
            self.conn: socket.socket | None = None
            print(f'Szerver elindult a következő címen: {host}:{port}')

    def wait_for_connection(self):
        self.listen()
        self.conn, addr = self.accept()
        print(f'Kapcsolódott: {addr}')

    def receive(self):
        data = self.conn.recv(1024)
        if data:
            return data.decode()

    def connect_to_server(self, host, port):
        self.connect((host, port))
        print(f'Kapcsolódás a szerverhez: {host}:{port}')

    def send_message(self, msg):
        self.sendall(msg.encode())

# def start_server():
#     server = ChessServer('0.0.0.0', 12345)
#     server.wait_for_connection()
#     server.receive()
