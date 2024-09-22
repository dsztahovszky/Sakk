import socket


def start_server(host='', port=40674):
    with socket.socket() as s:
        s.bind((host, port))
        s.listen(5)
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
