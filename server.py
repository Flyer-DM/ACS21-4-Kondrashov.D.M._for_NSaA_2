import socket
import random


def listen() -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    members = []
    average_port = 1025
    while True:
        try:
            sock.bind(('', average_port))
            print("Используется порт: " + str(average_port))
            break
        except OSError as error:
            print(f"{error} (порт {average_port} занят)")
            average_port = random.randint(1024, 65535)

while True:
    listen()