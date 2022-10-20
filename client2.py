import socket
import threading


stop = False


def listen(s: socket.socket) -> None:
    global stop
    while True:
        message = s.recv(1024).decode()
        if message == '$break':
            print("Disconnected.")
            stop = True
            break
        elif not message:
            stop = True
            break
        print('\r\r' + message + '\n' + 'you: ', end='')



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
            s.send(message.encode())
        if message == "exit":
            break
    s.close()


connect()
