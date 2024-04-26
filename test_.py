import socket
import json
import threading

import msgpack

class GameClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.list_player = {}  # Dictionary to store player information
        self.list_player_command = {}  # Dictionary to store player command

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            self.connected = True
            print("Connected to server.")
        except Exception as e:
            print("Error:", e)

    def send_data(self, data):
        if self.connected:
            try:
                # serialized_data = json.dumps(data)
                # self.socket.sendall(serialized_data.encode())
                serialized_data = msgpack.packb(data)
                self.socket.sendall(serialized_data)

            except Exception as e:
                print("Error:", e)
        else:
            print("Not connected to server.")

    def receive_data(self):
            # print("update")
            if self.connected:
                # try:
                        received_data = self.socket.recv(2048)
                        if received_data:
                            # decoded_data = json.loads(received_data.decode())
                            decoded_data = msgpack.unpackb(received_data)

                            # Update list_player_command and list_player
                            self.list_player_command = decoded_data.get("listPlayerCommand", {})
                            # print(self.list_player_command)
                            self.list_player = decoded_data.get("listPlayer", {})
                        else:
                            return None
                # except Exception as e:
                #     print("Error:", e)
                #     return None
            else:
                print("Not connected to server.")
                return None

    def handle_update(self):
        while True:
            if self.connected:

                        received_data = self.socket.recv(4096)
                        if received_data:
                            try:
                                # print("======")
                                # print(received_data.decode())
                                # decoded_data = json.loads(received_data.decode())
                                decoded_data = msgpack.unpackb(received_data)

                                # Update list_player_command and list_player
                                self.list_player_command = decoded_data["data"].get("listPlayerCommand", {})
                                self.list_player = decoded_data["data"].get("listPlayer", {})
                            except Exception as e:
                                print("Error decoding JSON:", str(e))
                        else:
                            return None

            else:
                print("Not connected to server.")
                return None

    def close(self):
        if self.connected:
            self.socket.close()
            self.connected = False
            print("Disconnected from server.")

    def get_list_player(self):
        return self.list_player

    def get_list_player_commmand(self):
        return self.list_player_command

from settings import *

class HubGame():
    def __init__(self,username):
        self.username = username
        self.client = GameClient(ONLINE_ADDRESS, ONLINE_PORT)  # Replace "localhost" with your server's IP address
        self.client.connect()
        receive_thread = threading.Thread(target=self.client.handle_update)
        receive_thread.daemon = True  # Đặt luồng thành daemon để nó sẽ kết thúc khi chương trình chính kết thúc
        receive_thread.start()

    def send_join(self,player_data):
        self.client.send_data(player_data)

    def send_data_command(self,player_data):
        self.client.send_data(player_data)
    
    def get_list_data(self):
        # self.client.receive_data()  # Update list_player_command and list_player
        return self.client.get_list_player()

    def get_list_data_command(self):
        # self.client.receive_data()  # Update list_player_command and list_player
        return self.client.get_list_player_commmand()
