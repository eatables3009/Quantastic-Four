import socket

def server_main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.184.106', 5555))
    server_socket.listen(2)  # Allow 2 clients to connect
    print("Server active")

    client_sockets = []  # List to store client sockets

    try:
        while len(client_sockets) < 2:
            client_socket, address = server_socket.accept()
            print(f"Connection from {address} has been established.")
            client_sockets.append(client_socket)

        while True:
            data = client_sockets[0].recv(4096)
            if not data:
                break  # Break the loop if no data is received

            print(f"Message: {data}")

            # Forward the encrypted message to Client 2
            client_sockets[1].sendall(data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        for client_socket in client_sockets:
            client_socket.close()

    server_socket.close()

if __name__ == "__main__":
    server_main()
