import random
import math
import numpy as np
import hashlib
import binascii

def eea(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = eea(b % a, a)
        return gcd, y - (b // a) * x, x


def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)


# алгоритм возведения в степень по модулю
def fast_power(a, b, n):
    if n == 1 and a != 0:
        return 0
    if a == 0:
        return 0
    if b == 0:
        return 1
    a = a % n
    res = 1
    while (b > 0):
        if ((b & 1) == 1):
            res = (res * a) % n
        b = b >> 1
        a = (a * a) % n
    return res


# определение длины циклов в тесте миллера и запуск k-раундов
def isPrime(n, k):
    if (n <= 1 or n == 4):
        return False
    if (n <= 3):
        return True
    t = n - 1
    while (t % 2 == 0):
        t //= 2
    for i in range(k):
        if miller_test(n, t) == False:
            return False
    return True


# алгоритм теста миллера-рабина на простоту
def miller_test(n, t):
    a = 2 + random.randint(1, n - 4)
    x = pow(a, t, n)
    if (x == 1 or x == n - 1):
        return True
    while (t != n - 1):
        x = (x ** 2) % n
        t *= 2
        if (x == 1):
            return False
        if (x == n - 1):
            return True
    return False


# запуск цикла с генерацией числа и добавлением +2 к нему, пока оно не станет вероят. простым
def gen_isPrime(n, k):
    result = isPrime(n, k)
    while result == False:
        n += 2
        k = int(math.ceil(math.log2(n)))
        result = isPrime(n, k)
    else:
        return n


def gen_keys(bits=512):
    p = random.getrandbits(bits)
    q = random.getrandbits(bits)
    if p % 2 == 0:
        p += 1
    if q % 2 == 0:
        q += 1
    p = gen_isPrime(p, int(math.ceil(math.log2(p))))
    q = gen_isPrime(q, int(math.ceil(math.log2(q))))
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(2, phi)
    g = np.gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = np.gcd(e, phi)
    _, d, __ = eea(e, phi)
    d = pow(d, 1, phi)
    return e, d, n, phi


def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


def rsa_encrypt(string, e, n_first, d, n_second):
    if n_first > n_second:
        n_second, n_first = n_first, n_second
        e, d = d, e
    cipher_text = string.encode('utf-8').hex()
    cipher = int(cipher_text, 16)
    h = pow(cipher, e, n_first)
    encrypted = pow(h, d, n_second)
    return encrypted


def rsa_decrypt(h, e, n_first, d, n_second):
    if n_first < n_second:
        n_second, n_first = n_first, n_second
        e, d = d, e
    cipher = pow(h, e, n_first)
    cipher_text = hex(pow(cipher, d, n_second)).rstrip("L")
    decrypted_text = binascii.unhexlify(cipher_text[2:])
    return decrypted_text
