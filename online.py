import json
import socket

from objects.board import Board
from objects.helpers import create_player
from objects.player_colour import PlayerColour
from utils.constants import COLS, ROWS, TOTAL_TOKENS
from utils.sockets import get_private_ip


def start_game(host="0.0.0.0", port=65433):
    host = get_private_ip()
    print("\nInitializing the game...")
    name1 = input("Enter Player 1 Name: ").strip()
    print("Creating Player 1...")
    player1 = create_player(name1, PlayerColour.RED, TOTAL_TOKENS)
    print(player1)
    board = Board(ROWS, COLS)
    game_data = {
        "player1": player1.to_dict(),
        "board": board.to_dict(),
        "status": "continue",
    }

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

            if "board" in json_data:
                board_json = json_data["board"]
                board = Board(board_json["rows"], board_json["cols"])
                board.from_dict(board_json["board"])

            if "status" in json_data and json_data["status"] == "finished":
                print("Game Over! Sorry You Lost!")
                break

            print(board)
            # Place the token and check for a win
            token = player1.remove_token()
            placed_row, placed_col = board.place_token(token, player1.name)
            game_data["board"] = board.to_dict()
            win = board.check(placed_row, placed_col, player1.colour)
            if win:
                print("Congradulations you've won")
                game_data["status"] = "finished"
                conn.sendall(json.dumps(game_data).encode())
                break
            conn.sendall(json.dumps(game_data).encode())
    finally:
        conn.close()  # Close the connection
        server_socket.close()
        print("Server closed.")


def join_game(host="192.168.0.15", port=65433):
    # Get Player 2 details and create the player object
    name1 = input("Enter Player 2 Name: ").strip()
    print("Creating Player 2...")
    player2 = create_player(name1, PlayerColour.YELLOW, TOTAL_TOKENS)
    print(player2)

    # Prepare JSON data to send
    json_data = {"player2": player2.to_dict()}

    print("\nJoining the game...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server.")

    try:
        # Send JSON data to the server
        client_socket.sendall(json.dumps(json_data).encode())
        print("Player data sent to server.")

        while True:
            # Receive and decode the server's response
            data = client_socket.recv(1024).decode()
            json_data = json.loads(data)
            if "status" in json_data and json_data["status"] == "finished":
                print("Game Over! Sorry You Lost!")
                break
            if "board" in json_data:
                board_json = json_data["board"]
                board = Board(board_json["rows"], board_json["cols"])
                board.from_dict(board_json["board"])
                print(board)
                token = player2.remove_token()
                placed_row, placed_col = board.place_token(token, player2.name)
                json_data["board"] = board.to_dict()
                win = board.check(placed_row, placed_col, player2.colour)
                if win:
                    print("Congradulations you've won")
                    json_data["status"] = "finished"
                    client_socket.sendall(json.dumps(json_data).encode())
                    break
                client_socket.sendall(json.dumps(json_data).encode())

    finally:
        client_socket.close()
        print("Connection closed.")
