import socket
import random
import datetime
import csv
import hashlib
import threading


members = []  # для рассылки сообщений всем подключённым клиентам


def logger(message: str) -> None:
    """Сохранение лог файла сервера"""
    with open('log.txt', 'a+') as f:  # лог файл
        f.write(message + ' | ' + str(datetime.datetime.now()) + '\n')
    print(message)


def send_to_all_clients(from_addr: tuple, message: str) -> None:
    """Функция отправки сообещний всем пользователям чата"""
    for i in members:
        if i != from_addr:
            i[0].send(message.encode())


def client_handling(sock: socket.socket, conn: socket.socket, addr: tuple) -> None:
    """Функция взаимодействия с клиентом"""
    conn.send("Введите ваше имя.".encode())
    user_name = conn.recv(1024).decode()
    logger("Подключение пользователя.")
    known = False
    with open("clients.csv", 'r') as clients_list:
        reader = csv.DictReader(clients_list)
        for row in reader:
            if row['name'] == user_name:
                user_password, user_name, known = row['password'], row['name'], not known
                logger("Подключение известного пользователя.")
                break
    if known:
        attempts = 3
        while True:
            if attempts == 0:
                conn.send("$break".encode())
                logger(f"Клиент {user_name} не подтвердил свой пароль.")
                conn.close()
                break
            conn.send("Введите ваш пароль.".encode())
            if hashlib.md5(conn.recv(1024)).hexdigest() == user_password:
                logger(f"Клиент {user_name} подтвердил свой пароль.")
                conn.send(f"Здравствуйте, {user_name}!".encode())
                break
            else:
                conn.send("Неверный пароль, попробуйте ещё раз.".encode())
                attempts -= 1
    else:
        logger("Начало регистрации нового пользователя.")
        conn.send(f"Здравствуйте, {user_name}! Создайте пароль.".encode())
        user_password = hashlib.md5(conn.recv(1024)).hexdigest()
        conn.send(f"Подтвердите ваш пароль.".encode())
        if hashlib.md5(conn.recv(1024)).hexdigest() == user_password:
            conn.send(f"Вы подтвердили ваш пароль.".encode())
            logger("Успешная регистрация нового пользователя.")
            with open("clients.csv", 'a+') as clients_list:
                writer = csv.DictWriter(clients_list, fieldnames=['name', 'password'])
                writer.writerow({'name': user_name, 'password': user_password})
        else:
            logger("Пользователь не оподтвердил свой пароль при регистрации и было отключён.")
            conn.send("$break".encode())
            conn.close()
    send_to_all_clients(addr, f"{user_name} подключился.")
    while True:
        try:
            data = conn.recv(1024).decode()
            if data == 'shutdown':
                logger(f"Завершение работы сервера клиентом {user_name}.")
                conn.close()
                sock.close()
                break
            if not data:
                logger("Отключение клиента: " + addr[0])
                conn.close()
                break
            else:
                logger(f"{user_name}: {data}")
                if data == 'exit':
                    send_to_all_clients(addr, f"{user_name} отключился.")
                else:
                    send_to_all_clients(addr, f"{user_name}: {data}")
        except (ConnectionError, OSError):  # очищение списка всех клиентов от вышедшего
            try:
                for i in range(len(members)):
                    if members[i] == addr:
                        members.pop(i)
                        break
            except BaseException:
                pass
            break


def bind_socket(sock: socket.socket) -> None:
    """Функция занимает свободный порт для заданного сокета"""
    average_port = 1025
    while True:
        try:
            sock.bind(('', average_port))
            print("Используется порт: " + str(average_port))
            break
        except OSError as error:
            print(f"{error} (порт {average_port} занят)")
            average_port = random.randint(1024, 65535)


def listen() -> None:
    """Функция создаёт сокет и ожидает входящие/исходящие сообщения"""
    try:
        sock = socket.socket()
        bind_socket(sock)
        sock.listen(10)
        logger("Включён режим прослушивания.")
        while True:
            conn, addr = sock.accept()
            logger(f"Присоединение клиента с ip {addr[0]}")
            members.append((conn, addr))
            threading.Thread(target=client_handling, args=(sock, conn, (conn, addr)), daemon=True).start()  # поток для каждого пользователя
    except OSError:
        pass


main_thread = threading.Thread(target=listen, name='main_thread')  # основной поток программы
main_thread.start()
