import json
import socket
import threading

import msgpack

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.clients_names={}
        self.listPlayer = {}
        self.listPlayerCommand = {}
        self.list_bullet ={}
        self.is_running = False

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Server is listening on {self.host}:{self.port}")
        self.is_running = True

        while self.is_running:
            client_socket, client_address = self.socket.accept()
            print(f"New connection from {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

    def handle_client(self, client_socket, client_address):
        while True:
            try:
                self.clients[client_address] = client_socket
                data = client_socket.recv(4096)
                if not data:
                    print(f"Connection with {client_address} closed")
                    del self.clients[client_address]

                    del self.listPlayer[self.clients_names[client_address]]
                    del self.listPlayerCommand[self.clients_names[client_address]]
                    break

                # print(f"Received data from {client_address}: {data.decode()}")
                # data = json.loads(data.decode())
                data = msgpack.unpackb(data)

                self.username = data["name"]
                self.clients_names[client_address] = self.username
                if "command" in data:
                    self.listPlayerCommand[data["name"]] = data
                else:
                    self.listPlayer[data["name"]] = data

                try:
                    print("=======")
                    data_to_send = {
                        "data":{
                            "listPlayerCommand": self.listPlayerCommand,
                            "listPlayer": self.listPlayer
                        }
                    }
                    print(data_to_send)
                    # data_to_send = json.dumps(data_to_send)
                    # client_socket.sendall(data_to_send.encode())
                    data_to_send = msgpack.packb(data_to_send)
                    client_socket.sendall(data_to_send)
                except Exception as e:
                    del self.clients[client_address]

                    del self.listPlayer[self.clients_names[client_address]]
                    del self.listPlayerCommand[self.clients_names[client_address]]


                # print(self.listPlayer)
                # self.broadcast_data()
            except Exception as e:
                print("bo qua loi du lieu "+str(e))
    def broadcast_data(self):
        data_to_send = {
            "data":{
                "listPlayerCommand": self.listPlayerCommand,
                "listPlayer": self.listPlayer
            }
        }
        # data_string = json.dumps(data_to_send)
        data_string = msgpack.packb(data_to_send)

        for client_socket in self.clients.values():
            client_socket.sendall(data_string)

    def stop(self):
        self.is_running = False
        self.socket.close()

from settings import *

if __name__ == "__main__":
    server = Server(ONLINE_ADDRESS, ONLINE_PORT)
    try:
        server.start()
    except KeyboardInterrupt:
        print("Server stopped")
        server.stop()
