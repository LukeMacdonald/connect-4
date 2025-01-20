import socket


def join_game(host="192.168.0.28", port=65432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server.")

    try:
        while True:
            # Get user input
            message = input("Enter message (type 'exit' to quit): ")

            # Send the message
            client_socket.sendall(message.encode())

            # Exit if the message is "exit"
            if message.strip().lower() == "exit":
                print("Exiting client.")
                break

            # Receive the server's response
            response = client_socket.recv(1024).decode()
            print(f"Server: {response}")
    finally:
        client_socket.close()
        print("Connection closed.")
    # Create a socket objec


join_game()
