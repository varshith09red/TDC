import socket
import threading

# Peer 2
host = '192.168.1.16'  # Listen on all available network interfaces
port = 12345

def receive_messages():
    while True:
        data, addr = server_socket.recvfrom(1024)
        print(f"Received: {data.decode()}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host, port))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    message = input("Enter your message: ")
    server_socket.sendto(message.encode(), ('192.168.1.16', 12346))  # Replace 'Peer1_IP' with the IP of the other peer
