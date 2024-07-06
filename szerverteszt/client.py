import socket


def start_client(host='176.63.5.255', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f'Kapcsolódás a szerverhez: {host}:{port}')

        while True:
            message = input("Írj egy üzenetet (vagy 'exit' a kilépéshez): ")
            if message.lower() == 'exit':
                break
            s.sendall(message.encode())
            data = s.recv(1024)
            print(f'Válasz: {data.decode()}')


if __name__ == "__main__":
    start_client()
