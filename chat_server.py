import socket
import threading

# Function to handle individual client connections
def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode().strip()
            print(f"Received message from {client_address}: {message}")
            broadcast(message, client_socket)
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break

    print(f"Connection from {client_address} closed.")
    client_socket.close()

# Function to broadcast message to all clients except the sender
def broadcast(message, sender_socket):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except Exception as e:
                print(f"Error broadcasting message to client: {e}")

# List to store client sockets
clients = []

# Server configuration
HOST = '192.168.184.136'  # Update with the desired IP address
PORT = 5555



# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server.bind((HOST, PORT))

# Listen for incoming connections
server.listen()

print(f"Server listening on {HOST}:{PORT}")

# Main server loop to accept client connections
while True:
    client_socket, client_address = server.accept()
    clients.append(client_socket)
    # Start a new thread to handle each client
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()
