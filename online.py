import json
import socket

from objects.board import Board
from objects.enums import PlayerColour
from objects.helpers import create_player
from objects.player import Player
from utils.constants import COLS, ROWS, TOTAL_TOKENS
from utils.sockets import get_private_ip


def start_game(player: Player, board: Board, port=65433):
    host = get_private_ip()
    print("\nInitializing the game...")
    game_data = {
        "player1": player.to_dict(),
        "board": board.to_dict(),
        "status": "continue",
    }

    # Set up server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        print(f"Server started at {host}:{port}")

        server_socket.listen(1)
        print("Waiting for a connection...")

        conn, addr = server_socket.accept()
        print(f"Connection established with {addr}")

        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break

                json_data = json.loads(data)

                if "player2" in json_data:
                    game_data["player2"] = json_data["player2"]

                if "board" in json_data:
                    board_json = json_data["board"]
                    board = Board(board_json["rows"], board_json["cols"])
                    board.from_dict(board_json["board"])

                if json_data.get("status") == "finished":
                    print("Game Over! Sorry You Lost!")
                    break

                print(board)
                token = player.remove_token()
                placed_row, placed_col = board.place_token(token, player.name)
                game_data["board"] = board.to_dict()

                if board.check(placed_row, placed_col, player.colour):
                    print("Congratulations, you've won!")
                    game_data["status"] = "finished"
                    conn.sendall(json.dumps(game_data).encode())
                    break

                conn.sendall(json.dumps(game_data).encode())
        finally:
            print("Server closed.")


def join_game(player: Player, host="192.168.0.15", port=65433):
    # Create Player 2

    json_data = {"player2": player.to_dict()}

    print("\nJoining the game...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print("Connected to server.")

        try:
            client_socket.sendall(json.dumps(json_data).encode())
            print("Player data sent to server.")

            while True:
                data = client_socket.recv(1024).decode()
                json_data = json.loads(data)

                if json_data.get("status") == "finished":
                    print("Game Over! Sorry You Lost!")
                    break

                if "board" in json_data:
                    board_json = json_data["board"]
                    board = Board(board_json["rows"], board_json["cols"])
                    board.from_dict(board_json["board"])
                    print(board)

                    token = player.remove_token()
                    placed_row, placed_col = board.place_token(token, player.name)
                    json_data["board"] = board.to_dict()

                    if board.check(placed_row, placed_col, player.colour):
                        print("Congratulations, you've won!")
                        json_data["status"] = "finished"
                        client_socket.sendall(json.dumps(json_data).encode())
                        break

                    client_socket.sendall(json.dumps(json_data).encode())
        finally:
            print("Connection closed.")
