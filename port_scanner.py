import socket
import threading
import re


result = []


def scanner(address: str, port: int) -> None:
    global result
    sock = socket.socket()
    sock.settimeout(0.5)
    try:
        sock.connect((address, port))
        result.append(port)
    except (ConnectionRefusedError, socket.timeout, ConnectionError, OSError):
        pass
    finally:
        sock.close()


def main(address: str) -> None:
    n = 65536 // 4096  # 16
    print("Сканирование портов: |", end='')
    for j in range(n - 1):
        for i in range(j * 4096, (j + 1) * 4096):
            try:
                p = threading.Thread(target=scanner, args=(address, i))
                p.start()
            except(RuntimeError):
                continue
        print('#', end='')
    print("| Сканирование завершено!")


hostname = input("Введите адрес хоста: ")
while True:
   if re.match('^(localhost)|(\d+\.\d+\.\d+\.\d+)$', hostname):
       break
   hostname = input("Неверный формат адреса, попробуйте ещё раз: ")


main(hostname)
print("Свободные порты:", *result)