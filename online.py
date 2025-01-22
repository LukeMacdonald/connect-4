import json
import socket

from objects.board import Board
from objects.player import Player
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
    try:
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
                        print("Connection closed by the client.")
                        break

                    try:
                        json_data = json.loads(data)
                    except json.JSONDecodeError:
                        print("Received invalid JSON data. Ignoring...")
                        continue

                    if "player2" in json_data:
                        game_data["player2"] = json_data["player2"]

                    if "board" in json_data:
                        try:
                            board_json = json_data["board"]
                            board = Board(board_json["rows"], board_json["cols"])
                            board.from_dict(board_json["board"])
                        except KeyError as e:
                            print(f"Invalid board data: {e}")
                            continue

                    if json_data.get("status") == "finished":
                        print("Game Over! Sorry You Lost!")
                        break

                    print(board)
                    token = player.remove_token()
                    placed_row, placed_col = board.players_turn(token, player.name)
                    game_data["board"] = board.to_dict()

                    if board.check(placed_row, placed_col, player.colour):
                        print("Congratulations, you've won!")
                        game_data["status"] = "finished"
                        conn.sendall(json.dumps(game_data).encode())
                        break

                    conn.sendall(json.dumps(game_data).encode())
            except Exception as e:
                print(f"Error during game loop: {e}")
            finally:
                print("Server closed.")
    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def join_game(player: Player, host="192.168.0.15", port=65433):
    # Create Player 2
    try:
        json_data = {"player2": player.to_dict()}

        print("\nJoining the game...")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((host, port))
                print("Connected to server.")

                client_socket.sendall(json.dumps(json_data).encode())
                print("Player data sent to server.")

                while True:
                    data = client_socket.recv(1024).decode()
                    if not data:
                        print("Connection closed by the server.")
                        break

                    try:
                        json_data = json.loads(data)
                    except json.JSONDecodeError:
                        print("Received invalid JSON data from the server. Ignoring...")
                        continue

                    if json_data.get("status") == "finished":
                        print("Game Over! Sorry You Lost!")
                        break

                    if "board" in json_data:
                        try:
                            board_json = json_data["board"]
                            board = Board(board_json["rows"], board_json["cols"])
                            board.from_dict(board_json["board"])
                            print(board)

                            token = player.remove_token()
                            placed_row, placed_col = board.players_turn(
                                token, player.name
                            )
                            json_data["board"] = board.to_dict()

                            if board.check(placed_row, placed_col, player.colour):
                                print("Congratulations, you've won!")
                                json_data["status"] = "finished"
                                client_socket.sendall(json.dumps(json_data).encode())
                                break

                            client_socket.sendall(json.dumps(json_data).encode())
                        except KeyError as e:
                            print(f"Invalid board data: {e}")
                            continue
            except socket.error as e:
                print(f"Error connecting to server: {e}")
            except Exception as e:
                print(f"Error during game loop: {e}")
            finally:
                print("Connection closed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
