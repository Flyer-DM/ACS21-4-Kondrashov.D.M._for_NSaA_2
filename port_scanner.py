import socket


def scanner(hostname: str) -> None:
    open_ports = []
    for i in range(50, 500):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        try:
            sock.connect((hostname, i))
            print(f"Порт {i} свободен")
            open_ports.append(i)
        except (ConnectionRefusedError, socket.timeout):
            continue
        finally:
            sock.close()
    print("Свободные порты:", *open_ports)


scanner('192.168.0.1')