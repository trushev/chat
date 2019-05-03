import sys
import socket
import threading

import kuznechik
import mqv


def _receiving(sock, name, key):
    while True:
        try:
            message = sock.recv(1024)
            if not message:
                print(f'{name} left the chat')
                return
            message = kuznechik.decrypt_text(message, key)
            print(f'{name} says: {message}')
        except Exception as e:
            return e


def _sending(sock, key):
    while True:
        try:
            message = input()
            message = kuznechik.encrypt_text(message, key)
            sock.send(message)
        except KeyboardInterrupt:
            sock.close()
            return


def _parse_host():
    host = input('Enter address:port ')
    host = host.split(':')
    if not host[0]:
        return socket.gethostbyname(socket.gethostname()), 9090
    return host[0], int(host[1])


def start_chat():
    address, port = _parse_host()
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((address, port))
    server_socket.listen(1)
    print(f'Started at {address}:{port}')

    while True:
        client_socket, client_address = server_socket.accept()
        print('Bob connected to the chat\n')

        shared_key = mqv.start_handshake(client_socket)
        shared_key = kuznechik.expand_key(shared_key)

        receiving_thread = threading.Thread(target=_receiving, args=(client_socket, 'Bob', shared_key))
        receiving_thread.start()
        _sending(client_socket, shared_key)


def connect_to_chat():
    address, port = _parse_host()
    sock = socket.socket()
    sock.connect((address, port))
    print(f'Connected to the chat at {address} {port}\n')

    shared_key = mqv.accept_handshake(sock)
    shared_key = kuznechik.expand_key(shared_key)

    receiving_thread = threading.Thread(target=_receiving, args=(sock, 'Alice', shared_key))
    receiving_thread.start()
    _sending(sock, shared_key)


if __name__ == '__main__':
    assert len(sys.argv) == 2, 'start or connect'

    if sys.argv[1] == 'start':
        start_chat()
    elif sys.argv[1] == 'connect':
        connect_to_chat()
    else:
        assert False, 'start or connect'
