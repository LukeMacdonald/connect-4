import socket


def start_game(host="0.0.0.0", port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(((host, port)))
    print(f"Server started at {host}:{port}")

    # Start listening for incoming connections (max 1 connection in the queue)
    server_socket.listen(1)
    print("Waiting for a connection...")

    # Accept the connection (blocks until a connection is made)
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    # Send a welcome message
    client_socket.send(b"Hello from the server!")

    # Receive data from the client (max buffer size is 1024 bytes)
    data = client_socket.recv(1024)
    print(f"Received from client: {data.decode()}")
    # Close the connection

    client_socket.close()
    server_socket.close()


start_game()
