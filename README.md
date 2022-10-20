Лабораторная работа "Многопоточный сервер" по ССиП


1. Сканнер TCP-портов:

![image](https://user-images.githubusercontent.com/113033685/196955470-d848d80c-cc15-49a7-b9d3-8814b80ba0ed.png)

Сканирование портов разбивается на несколько потоков:

![image](https://user-images.githubusercontent.com/113033685/196955524-7e03e469-2a1f-45e2-b16b-6ad304ab8844.png)

Вывод идёт по порядку.
Добавлен заполняющийся progress bar.

![image](https://user-images.githubusercontent.com/113033685/196955575-7c1921df-60b9-4dde-a938-ed434f881ba0.png)

2. Для каждого клиента на сервере создаётся отдельный поток.

![image](https://user-images.githubusercontent.com/113033685/196955636-be018954-0310-4649-b6a9-bf7a54127abf.png)

3. Реализовать простой чат сервер на базе сервера аутентификации. Сервер должен обеспечивать подключение многих пользователей одновременно, отслеживание имен пользователей, поддерживать историю сообщений и пересылку сообщений от каждого пользователя всем остальным.

Первичное подключение клиента:

![image](https://user-images.githubusercontent.com/113033685/196955791-eeb75886-6ce3-4591-9abe-ff6974a898ed.png)

![image](https://user-images.githubusercontent.com/113033685/196955805-dcadda8e-983f-4513-b746-b68d91a0afa9.png)

Отключение клиента от сервера командой exit:

![image](https://user-images.githubusercontent.com/113033685/196955842-962fd2ac-802d-4bef-9be3-eeb33de640fd.png)

Повторное подключение к серверу и его отключение командой shutdown:

![image](https://user-images.githubusercontent.com/113033685/196955924-8b0ca8c7-d236-4e13-8890-1bd46658019b.png)

Хранение лог файла:

![image](https://user-images.githubusercontent.com/113033685/196956005-4c31034e-f49c-4450-983e-aef0f9acae0c.png)

Безопасное хранение паролей в отдельном файле:

![image](https://user-images.githubusercontent.com/113033685/196956042-2252fb4a-a448-4e9a-955a-cc14f257c0bc.png)

Подключение нескольких клиентов одновременно:

![image](https://user-images.githubusercontent.com/113033685/196956098-7247f18b-502d-490d-b6a4-c835501c6e9a.png)

4. Сервер с управляющим потоком:

![image](https://user-images.githubusercontent.com/113033685/196956160-21b4b902-d913-4d76-beac-3b993dc21101.png)

Отключение одного клиента от сервера:

![image](https://user-images.githubusercontent.com/113033685/196956219-e165b8fd-34f2-461d-921d-d00e25944574.png)

Отключение сервера последним клиентом:

![image](https://user-images.githubusercontent.com/113033685/196956303-f868ca29-7649-495d-839a-50b7f7733e6e.png)

Обработка неверного ввода пароля (3 попытки):

![image](https://user-images.githubusercontent.com/113033685/196956347-d55af4a5-8c63-4dae-b090-bf4af221189f.png)
