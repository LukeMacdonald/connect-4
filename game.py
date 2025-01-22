from objects.board import Board
from objects.enums import GameOptions, PlayerColour
from objects.helpers import create_computer, create_player, swap_player
from objects.player import Computer, Player
from online import join_game, start_game
from utils.constants import COLS, ROWS, TOTAL_TOKENS


def menu():
    """
    Display the game menu and get the user's choice.
    """
    while True:
        print("\nConnect 4")
        print("-" * 20)
        print("1: Start a New Game")
        print("2: Start an Online Game")
        print("3: Join an Online Game")
        print("4: Play against Computer")
        print("5: Exit")
        try:
            option = int(input("Choose an option: "))
            if option in [1, 2, 3, 4, 5]:
                return option
            else:
                print("Invalid choice. Please choose a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def init_game(option: GameOptions):
    """
    Initialize the game by creating players and the game board.
    """
    player1 = None
    player2 = None
    if option != GameOptions.JOIN:
        print("\nInitializing the game...")
        name1 = input("Enter Player 1 Name: ").strip()
        print("Creating Player 1...")
        player1 = create_player(name1, PlayerColour.RED, TOTAL_TOKENS)
        print(player1)
    if option == GameOptions.OFFLINE or option == GameOptions.JOIN:
        name2 = input("Enter Player 2 Name: ").strip()
        print("Creating Player 2...")
        player2 = create_player(name2, PlayerColour.YELLOW, TOTAL_TOKENS)
        print(player2)
    if option == GameOptions.COMPUTER:
        player2 = create_computer(TOTAL_TOKENS)

    board = Board(ROWS, COLS)
    print("Game board created:\n")
    print(board)
    return player1, player2, board


def play_game(current_player, other_player, board):
    """
    Main game loop to handle the Connect 4 gameplay.
    """
    while True:
        print(f"\n{current_player.name}'s turn ({current_player.colour.name})")
        print(board)

        if not current_player.has_tokens():
            print(f"{current_player.name} has no tokens left. Skipping turn...")
            current_player, other_player = swap_player(current_player, other_player)
            continue

        # Place the token and check for a win
        token = current_player.remove_token()
        placed_row, placed_col = board.players_turn(token, current_player.name)

        win = board.check(placed_row, placed_col, current_player.colour)
        if win:
            print(
                f"\nPlayer {current_player.name} ({current_player.colour.name}) has won!"
            )
            print(board)
            return

        # Swap players
        current_player, other_player = swap_player(current_player, other_player)


def play_computer(player: Player, computer: Computer, board: Board):
    print(player)
    print(computer)
    print(board)
    while True:
        player_token = player.remove_token()
        placed_row, placed_col = board.players_turn(player_token, player.name)

        win = board.check(placed_row, placed_col, player.colour)
        if win:
            print(f"\nPlayer {player.name} ({player.colour.name}) has won!")
            print(board)
            return
        print(board)
        computer_token = computer.remove_token()


# Main program execution
if __name__ == "__main__":
    while True:
        choice = menu()
        if choice == 1:
            p1, p2, board = init_game(GameOptions.OFFLINE)
            play_game(p1, p2, board)
        elif choice == 2:
            p1, _, board = init_game(GameOptions.ONLINE)
            if not isinstance(p1, Player):
                break
            start_game(p1, board)
        elif choice == 3:
            _, p2, _ = init_game(GameOptions.JOIN)
            if not isinstance(p2, Player):
                break
            join_game(p2)
        elif choice == 4:
            p1, computer, board = init_game(GameOptions.COMPUTER)
            if not isinstance(p1, Player) or isinstance(computer, Computer):
                break
            play_computer(p1, computer, board)
        elif choice == 5:
            print("Exiting the game. Goodbye!")
            break
        else:
            print("This feature is not yet implemented. Please try another option.")
