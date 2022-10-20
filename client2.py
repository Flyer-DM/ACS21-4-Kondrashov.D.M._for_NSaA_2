import socket
import threading


stop = False


def listen(s: socket.socket) -> None:
    global stop
    while True:
        try:
            message = s.recv(1024).decode()
            if message in ('$break', 'shutdown'):
                print("Disconnected.")
                stop = True
                break
            elif not message:
                stop = True
                break
            print('\r\r' + message + '\n' + 'you: ', end='')
        except ConnectionResetError:
            print("Server off.")
            stop = True
            break


def connect(host: str = '127.0.0.1', port: int = 1025) -> None:
    global stop
    s = socket.socket()
    s.connect((host, port))
    threading.Thread(target=listen, args=(s,), daemon=True).start()
    while True:
        message = input('you: ')
        if stop:
            break
        else:
            try:
                s.send(message.encode())
            except ConnectionResetError:
                pass
        if message in ('exit', 'shutdown'):
            break
    s.close()


connect()
