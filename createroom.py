import socket
import threading
import random
import string

# Your existing code for colors and fonts
DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = 'white'
FONT = ("Helvetica", 17)
SMALL_FONT = ("Helvetica", 13)

HOST = '127.0.0.1'  # Change this to the actual server IP
PORT = 8080

# Function to generate a random room code
def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Function to handle communication within the room
def communicate_in_room(client, room_code):
    username = input("Enter your username: ")
    if username != '':
        client.sendall(username.encode())
    else:
        print("Username cannot be empty")
        exit(0)

    threading.Thread(target=listen_for_messages_from_room, args=(client, room_code)).start()
    send_message_to_room(client, room_code)

# Function to listen for messages within the room
def listen_for_messages_from_room(client, room_code):
    while True:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            print(f"[Room {room_code}] {message}")
        else:
            print(f"Message received from room {room_code} is empty")

# Function to send messages to the room
def send_message_to_room(client, room_code):
    while True:
        message = input(f"[Room {room_code}] Enter your message: ")
        if message != '':
            client.sendall(message.encode())
        else:
            print("Empty message")
            exit(0)

# Function to create and join a room
def create_and_join_room():
    room_code = generate_room_code()
    print(f"Your room code is: {room_code}")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print(f"Successfully connected to the server")
    except:
        print(f"Unable to connect to the server {HOST} {PORT}")
        exit(0)

    # Join the room
    client.sendall(f"JOIN~{room_code}".encode())

    # Communicate within the room
    communicate_in_room(client, room_code)

# Main function
def main():
    create_and_join_room()

if __name__ == '__main__':
    main()
