import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 5555

server_socket.bind((host, port))
server_socket.listen()

print(f"Server is listening on {host}:{port}")

rooms = {}

def handle_client(client_socket, addr):
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            parts = data.split()
            command = parts[0]

            if command == "CREATE_ROOM":
                room_code = parts[1]
                if room_code not in rooms:
                    rooms[room_code] = []
                    print(f"Room {room_code} created by {addr}")
                    client_socket.send("ROOM_CREATED".encode('utf-8'))
                    broadcast_to_clients(f"ROOM_CREATED {room_code}")
                else:
                    client_socket.send("ROOM_EXISTS".encode('utf-8'))

    except Exception as e:
        print(f"Connection error from {addr}: {str(e)}")
    finally:
        client_socket.close()

def broadcast_to_clients(message):
    for client, _ in rooms.values():
        client.send(message.encode('utf-8'))

def accept_clients():
    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection established from {addr}")
            
            # Store client socket and address in rooms dictionary
            rooms[addr] = (client_socket, addr)

            # Create a thread to handle the client connection
            client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_handler.start()

    except Exception as e:
        print(f"Server error: {str(e)}")
    finally:
        server_socket.close()

# Start listening for and accepting client connections
accept_clients()
