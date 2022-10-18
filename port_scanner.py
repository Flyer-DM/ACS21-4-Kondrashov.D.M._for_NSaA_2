import socket
import threading
import time
import re


def scanner(hostname: str, port: str) -> None:
    sock = socket.socket()
    sock.settimeout(0.5)
    try:
        sock.connect((hostname, port))
        print(f"Порт {port} свободен")
    except (ConnectionRefusedError, socket.timeout, ConnectionError, OSError):
        pass
    finally:
        sock.close()



hostname = input("Введите адрес хоста: ")
while True:
    if re.match('^localhost|(\d{3}\.\d{3}\.\d{3}\.\d{3})$', hostname):
        break
    hostname = input("Неверный формат адреса, попробуйте ещё раз: ")
start_time = time.time()
for i in range(1, 65536):
    try:
        p = threading.Thread(target=scanner, args=(hostname, i))
        p.start()
    except(RuntimeError):
        continue
print("Время работы программы:", round(time.time() - start_time))
