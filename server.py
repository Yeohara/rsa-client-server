import socket, pickle
from model import gen_keys
from model import encrypt_string
from model import rsa_decrypt

bits = 512
users = ["Kirill"]
passwords = [encrypt_string("12345")]
sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
e, d, n, phi = gen_keys(bits)

print('Открытый ключ сервера: e = {}, n = {}'.format(e, n))
print('Закрытый ключ сервера: d = {}, n = {}'.format(d, n))

while True:
    conn, addr = sock.accept()
    e_client = conn.recv(10000)
    e_client = int(e_client)
    n_client = conn.recv(10000)
    n_client = int(n_client)
    print('Открытый ключ клиента: e = {}, n = {}'.format(e_client, n_client))
    conn.send(str.encode(str(e)))
    conn.send(str.encode(str(n)))
    while True:
        log_pass = conn.recv(10000)
        log_pass = pickle.loads(log_pass)
        login = log_pass[0]
        password = log_pass[1]
        login = rsa_decrypt(login, e_client, n_client, d, n)
        password = rsa_decrypt(password, e_client, n_client, d, n)
        login = login.decode()
        password = password.decode()
        print("Полученный логин: ", login)
        print("Полученный пароль: ", password)
        if login == users[0]:
            if password == passwords[0]:
                print("Авторизация прошла успешно")
                conn.send(str.encode("Авторизация прошла успешно"))
                auth = True
                break
            else:
                print("Неправильный логин или пароль")
                conn.send(str.encode("Неправильный логин или пароль"))
        else:
            print("Неправильный логин или пароль")
            conn.send(str.encode("Неправильный логин или пароль"))
    while auth:
        message = conn.recv(10000)
        message = pickle.loads(message)
        message = rsa_decrypt(message, e_client, n_client, d, n).decode()
        if message == "exit":
            print("Клиент отключился")
            break
        print("Пришло сообщение от клиента: ", message)
        conn.send(str.encode("Ваше сообщение : '{}' было успешно доставлено".format(message)))
    conn.close()
    break
