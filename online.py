import socket


def start_game(host="0.0.0.0", port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(((host, port)))
    print(f"Server started at {host}:{port}")

    # Start listening for incoming connections (max 1 connection in the queue)
    server_socket.listen(1)
    print("Waiting for a connection...")

    # Accept the connection (blocks until a connection is made)
    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")
    try:
        while True:
            # Receive data
            data = conn.recv(1024).decode()
            if not data:  # Connection closed by client
                break

            print(f"Received: {data}")

            # Check for a termination condition
            if data.strip().lower() == "exit":  # Custom condition
                print("Exit command received. Closing connection.")
                conn.sendall("Goodbye!".encode())
                break

            # Echo the data back to the client (optional)
            conn.sendall(f"Echo: {data}".encode())
    finally:
        conn.close()  # Close the connection
        server_socket.close()
        print("Server closed.")


start_game()
