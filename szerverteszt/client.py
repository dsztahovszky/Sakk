import socket


def start_client(host=input('Szerver IP-címe: '), port=40674):
    with socket.socket() as s:
        s.connect((host, port))
        print(f'Kapcsolódás a szerverhez: {host}:{port}')

        while True:
            # message = input("Írj egy üzenetet (vagy 'exit' a kilépéshez): ")
            # if message.lower() == 'exit':
            #     break
            # s.sendall(message.encode())
            data = s.recv(1024)
            if data:
                print(f'Válasz: {data.decode()}')
            else:
                break


if __name__ == "__main__":
    start_client()
