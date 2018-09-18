'''
TODO move socketerror handler here
'''
import socket


class Socket:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created. Setting the socket...")
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("Done. Binding the port...")
        self.sock.bind(("", self.port))
        print("Port has been bind. Start listening...")
        self.sock.listen(1)
        print("Listening done. Retrieving conn and addr...")
        self.conn, self.client_address = self.sock.accept()
        print("Done!")

    def receive(self):
        data = self.conn.recv(1024)
        data = data.decode()
        return data

    def send(self, data):
        data = data.encode()
        self.conn.send(data)

    def disconnect(self):
        print("Client disconnected by demand")
        print("Restarting sockets...")
        self.conn.close()
        print("Connection closed. Initializing socket...")