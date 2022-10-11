import socket
import threading


def scanner(hostname: str, port: str) -> None:
    open_ports = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        sock.connect((hostname, port))
        print(f"Порт {port} свободен")
        open_ports.append(port)
    except (ConnectionRefusedError, socket.timeout):
        pass
    finally:
        sock.close()



hostname = '192.168.0.1'
for i in range(1, 1000):
    p = threading.Thread(target=scanner, args=(hostname, i))
    p.start()
