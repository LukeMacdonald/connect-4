import json
import socket

from board import Board
from game import TOTAL_TOKENS, create_player
from utils import PlayerColour


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
            if "board" in json_data:
                board_json = json_data["board"]
                board = Board(board_json["rows"], board_json["cols"])
                board.from_dict(board_json["board"])
                print(board)

    finally:
        client_socket.close()
        print("Connection closed.")


if __name__ == "__main__":
    join_game()
