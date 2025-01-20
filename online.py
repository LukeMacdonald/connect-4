import json
import socket

import board
from board import Board
from game import COLS, ROWS, TOTAL_TOKENS, create_player
from utils import PlayerColour


def start_game(host="0.0.0.0", port=65432):
    print("\nInitializing the game...")
    name1 = input("Enter Player 1 Name: ").strip()
    print("Creating Player 1...")
    player1 = create_player(name1, PlayerColour.RED, TOTAL_TOKENS)
    print(player1)
    board = Board(ROWS, COLS)
    game_data = {"player1": player1.to_dict(), "board": board.to_dict()}

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
            json_data = json.loads(data)
            if "player2" not in json_data:
                break
            print(json_data)
            game_data["player2"] = json_data["player2"]
            # Check for a termination condition
            if data.strip().lower() == "exit":  # Custom condition
                print("Exit command received. Closing connection.")
                conn.sendall("Goodbye!".encode())
                break
            conn.sendall(json.dumps(game_data).encode())
    finally:
        conn.close()  # Close the connection
        server_socket.close()
        print("Server closed.")


start_game()
