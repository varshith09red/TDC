# from secp256k1Crypto import curve,scalar_mult, point_add
# import random
# import hashlib
# import sys

import json
import socket
import threading

from zkp import ZKProof

# User class to store user information
class User:
    def __init__(self, username, ip, port, auth):
        self.username = username
        self.ip = ip
        self.port = port
        self.auth = auth

    def __str__(self):
        return f"UserName: {self.username}, IP: {self.ip}, Port: {self.port}, Auth: {self.auth}"


# Peer 1
host = '192.168.1.16'  # Listen on all available network interfaces
port = 15000

# Dictionary to store users in the network
users_file = 'users.json'
users = {}

def read_user_file():
    try:
        with open(users_file, 'r') as file:
            users_data = json.load(file)
            users = {user_data['username']: User(**user_data) for user_data in users_data}
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}
    return users

users = read_user_file()

def save_users_to_file():
    with open(users_file, 'w') as file:
        json.dump([user.__dict__ for user in users.values()], file, indent=4)

def receive_messages():
    while True:
        data, addr = server_socket.recvfrom(1024)
        message = data.decode()
        print(f"Msg received from {message}")
        if message.lower() == 'exit':
            print("Exiting...")
            server_socket.close()
            exit()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Find an available port
while True:
    try:
        if port > 65535:
            print("Error: No available port found.")
            exit()

        server_socket.bind((host, port))
        break
    except socket.error as e:
        if e.errno:  # Address already in use
            port += 1
        else:
            print(f"Error binding to port {port}: {e}")
            exit()

print(f"Bound to port {port}")

zkp = ZKProof()
salt = zkp.getSalt()
print(f"salt: {salt}")
ip = host  # You may need to modify this based on your network configuration
# Check if the user already exists
username = input("Enter your username: ")
if username in users:
    print(f"Welcome back, {username}!")
    auth = users[username].auth

    #is already authenticated
    if auth == 1:
        secret_card = 'spade_two' # Here we define the secret card
        x = zkp.generate_proof(secret_card, salt)
        print('Proof:', x)
    
    
else:
    print(f"New user! Please set up your authentication information.")
    while True:
        secret = input("Enter your authentication information: ")

        if secret.lower() == 'exit':
            print("Exiting...")
            exit()

        if(zkp.verify(secret, salt)):
            auth = 1
            print(f"Auth Passed!....New user added to the group!")
        else:
            print(f"Auth Failed!....Please try again")

# Create a User object for the current peer
current_user = User(username, ip, port, auth)
users[current_user] = current_user
save_users_to_file()

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    print("Connected Users:")
    users = read_user_file()
    for user in users.values():
        print(f"- {user}")
    
    dest_username = input("Enter the username of the destination user (type 'exit' to quit): ")

    if dest_username.lower() == 'exit':
        print("Exiting...")
        # server_socket.sendto('exit'.encode(), (host, port))
        server_socket.close()
        exit()

    dest_port = users[dest_username].port if dest_username in users else port
    # print("Dest Port: ",dest_port )
    message = input("Enter your message: ")

    server_socket.sendto(f"{current_user.username}: {message}".encode(), (host, dest_port))
