import socket
import threading


def listen(s: socket.socket) -> None:
    while True:
        message = s.recv(1024).decode()
        if message.startswith('b$'):
            print('\r\r' + message[2:])
            break
        print('\r\r' + message + '\n' + 'you: ', end='')


def connect(host: str = '127.0.0.1', port: int = 1025) -> None:
    s = socket.socket()
    s.connect((host, port))
    threading.Thread(target=listen, args=(s,), daemon=True).start()
    while True:
        message = input('you: ')
        s.send(message.encode())
        if message == "exit":
            break


connect()
