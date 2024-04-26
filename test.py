import json
import socket
from settings import *
def receive_data():
    host = ONLINE_ADDRESS
    port = ONLINE_PORT  # Port của server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            data_received = json.loads(data.decode())
            # Xử lý dữ liệu nhận được ở đây
            print("Received data:", data_received)
    except KeyboardInterrupt:
        print("Client stopped")
    finally:
        client_socket.close()

if __name__ == "__main__":
    receive_data()
