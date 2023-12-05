
import socket


class TCPClient():
    _server_authenticate_timeout = 5
    _server_keepalive_timeout = 3600
    _server_authenticate_username = "arx"
    _server_authenticate_password = "arx"

    def __init__(self, server_ip, server_port) -> None:
        self._server_ip = server_ip
        self._server_port = server_port
        self._is_connected = False

    def __del__(self):
        self.close()

    def connect(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.settimeout(self._server_authenticate_timeout)
        self._client.connect((self._server_ip, self._server_port))
        self._client.send("{}/{}".format(self._server_authenticate_username,
                          self._server_authenticate_password).encode())
        response = self._client.recv(1024).decode()
        print(response)
        if response == '0':
            self._client.close()
            return False
        self._client.settimeout(self._server_keepalive_timeout)
        self._is_connected = True
        return self._is_connected

    def close(self):
        if self._is_connected:
            self._client.close()

    def handle(self):
        while self._is_connected:
            data = input("> ")
            if not data:
                break
            self._client.send(data.encode())
            response = self._client.recv(1024).decode()
            print(response)


client=TCPClient('127.0.0.1',2345)
client.connect()
client.handle()
client.close()
