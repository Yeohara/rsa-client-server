import socket, pickle
from model import gen_keys
from model import encrypt_string
from model import rsa_encrypt

bits = 512
sock = socket.socket()
sock.connect(('localhost', 9090))
e, d, n, phi = gen_keys(bits)

print('Открытый ключ клиента: e = {}, n = {}'.format(e, n))
print('Закрытый ключ клиента: d = {}, n = {}'.format(d, n))

sock.send(str.encode(str(e)))
sock.send(str.encode(str(n)))
e_server = sock.recv(10000)
e_server = int(e_server)
n_server = sock.recv(10000)
n_server = int(n_server)
print('Открытый ключ сервера: e = {}, n = {}'.format(e_server, n_server))
while True:
    login = input("Введите ваш логин: ")
    password = input("Введите ваш пароль: ")
    password = encrypt_string(password)
    login = rsa_encrypt(login, e_server, n_server, d, n)
    password = rsa_encrypt(password, e_server, n_server, d, n)
    log_pass = (login, password)
    log_pass = pickle.dumps(log_pass)
    sock.send(log_pass)
    response = sock.recv(4096).decode()
    print('Ответ сервера: ', response)
    if response == "Неправильный логин или пароль":
        continue
    else:
        break
while True:
    message = input("Введите ваше сообщение: ")
    if message == "exit":
        message = (rsa_encrypt(message, e_server, n_server, d, n))
        message = pickle.dumps(message)
        sock.send(message)
        break
    message = (rsa_encrypt(message, e_server, n_server, d, n))
    message = pickle.dumps(message)
    sock.send(message)
    response = sock.recv(4096)
    print("Ответ сервера: ", response.decode())
sock.close()
