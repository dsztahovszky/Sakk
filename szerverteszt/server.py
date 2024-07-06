import socket


def start_server(host='0.0.0.0', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f'Szerver elindult a következő címen: {host}:{port}')

        conn, addr = s.accept()
        with conn:
            print(f'Kapcsolódott: {addr}')
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f'Üzenet: {data.decode()}')
                conn.sendall(data)  # Echo back the received data


if __name__ == "__main__":
    start_server()
