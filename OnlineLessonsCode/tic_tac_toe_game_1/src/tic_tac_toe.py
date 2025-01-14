print("Welcome to Tic Tac Toe!")

import random

def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return True
    for column in range(3):
        if board[0][column] == board[1][column] == board[2][column] != ' ':
            return True
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return True
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return True
    return False

def main():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    for _ in range(9):
        print_board(board)
        if current_player == 'X':
            row = int(input(f"Player {current_player}, enter the row (0, 1, 2): "))
            col = int(input(f"Player {current_player}, enter the column (0, 1, 2): "))
        else:
            row, col = get_computer_move(board)
            print(f"Computer plays at ({row}, {col})")

        if board[row][col] == ' ':
            board[row][col] = current_player
            if check_winner(board):
                print_board(board)
                print(f"Player {current_player} wins!")
                return
            current_player = 'O' if current_player == 'X' else 'X'
        else:
            print("This position is already taken. Try again.")
    print_board(board)
    print("It's a draw!")

def get_computer_move(board):
    empty_positions = [(r, c) for r in range(3) for c in range(3) if board[r][c] == ' ']
    return random.choice(empty_positions)

if __name__ == "__main__":
    main()