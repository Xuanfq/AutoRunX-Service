
import socket
import threading
import time
from threading import Thread


class TCPServer(Thread):
    _server_authenticate_timeout = 5
    _server_keepalive_timeout = 3600
    _server_authenticate_username = "arx"
    _server_authenticate_password = "arx"

    def __init__(self, listen_port: int, max_connections: int, listen_ip='0.0.0.0', client_handler=None) -> None:
        Thread.__init__(self)
        self._bind_ip = listen_ip
        self._bind_port = listen_port
        self._max_connections = max_connections
        self._client_handler = client_handler if client_handler is not None else self._client_handler

    def run(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.bind((self._bind_ip, self._bind_port))
        self._server.listen(self._max_connections)
        print("[*] Listening on {}:{}".format(self._bind_ip, self._bind_port))
        while True:
            # wait for connection
            client_socket, addr = self._server.accept()
            print("[*] Acception connection from {}:{}".format(addr[0], addr[1]))
            client_handler = threading.Thread(target=self._client_handler, 
                                              args=(client_socket, addr))
            client_handler.start()

    def _client_handler(self, client_socket: socket.socket, addr):
        def send(data):
            client_socket.send(data.encode())

        def recv(size=1024):
            return client_socket.recv(size).decode()

        def close():
            client_socket.close()

        def authenticate():
            client_socket.settimeout(self._server_authenticate_timeout)
            # id
            id = recv()
            
            # login
            username, password = recv().split('/')
            if username == self._server_authenticate_username and password == self._server_authenticate_password:
                send('1')
                return True
            else:
                send('0')
                return False

        def do_option():
            client_socket.settimeout(self._server_keepalive_timeout)
            while True:
                cmd = recv()
                print(cmd)
                send('1')
                # if cmd == 'local'

        try:
            if not authenticate():
                close()
            do_option()
            close()
        except Exception as e:
            print(e)


server = TCPServer(2345, 10)
server.start()
print('runing....')
# while True:
#     print('runing....')
#     time.sleep(10)


# 1. client send user/password
