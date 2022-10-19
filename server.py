import socket
import random
import datetime
import csv
import hashlib
import threading


f = open('log.txt', 'w')


def logger(message: str) -> None:
    f.write(message + ' | ' + str(datetime.datetime.now()) + '\n')
    print(message)


def client_handling(conn: socket.socket) -> None:
    conn.send("Введите ваше имя: ".encode())
    user_name = conn.recv(1024).decode()  # получение имени пользователя
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
                conn.send("b$Количество попыток исчерпано!".encode())
                logger(f"Клиент {user_name} не подтвердил свой пароль.")
                conn.close()
            conn.send("Введите ваш пароль: ".encode())
            if hashlib.md5(conn.recv(1024)).hexdigest() == user_password:
                logger(f"Клиент {user_name} подтвердил свой пароль.")
                conn.send(f"Здравствуйте, {user_name}!")
            else:
                attempts -= 1
    else:
        logger("Начало регистрации нового пользователя.")
        conn.send(f"Здравствуйте, {user_name}! Создайте пароль: ".encode())
        user_password = hashlib.md5(conn.recv(1024)).hexdigest()
        conn.send(f"Подтвердите ваш пароль: ".encode())
        if hashlib.md5(conn.recv(1024)).hexdigest() == user_password:
            conn.send(f"Вы подтвердили ваш пароль.".encode())
            logger("Успешная регистрация нового пользователя.")
            with open("clients.csv", 'a+') as clients_list:
                writer = csv.DictWriter(clients_list, fieldnames=['name', 'password'])
                writer.writerow({'name': user_name, 'password': user_password})
        else:
            conn.send("b$Вы не подтвердили свой пароль! Переподключитесь.".encode())
            conn.close()


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
    sock = socket.socket()
    members = []  # для рассылки сообщений всем подключённым клиентам
    bind_socket(sock)
    sock.listen(10)
    logger("Включён режим прослушивания.")
    while True:
        conn, addr = sock.accept()
        logger(f"Присоединение клиента с ip {addr[0]}")
        members.append((conn, addr))
        threading.Thread(target=client_handling, args=(conn, )).start()


listen()

f.close()