import socket


def join_game(server_host="192.168.0.28", server_port=65432):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((server_host, server_port))

    # Receive and print the welcome message from the server
    welcome_msg = client_socket.recv(1024)
    print(f"Received from server: {welcome_msg.decode()}")

    # Send a message to the server
    client_socket.send(b"Hello from the client!")

    # Close the connection
    client_socket.close()


join_game()
