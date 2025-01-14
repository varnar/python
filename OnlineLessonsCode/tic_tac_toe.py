# declare board
board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]

def print_board(board):
    print('   C0  C1  C2 ')
    raw_line = '  ---+---+---'
    print(raw_line)
    count = 0
    for row in board:
        print(f'R{count} {row[0]} | {row[1]} | {row[2]}')
        count += 1
        print(raw_line)

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return True
    for column in range(3):
        if board[0][column] == board[1][column] == board[2][column] != ' ':
            return True
    # check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return True
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return True
    return False

def main():
    # main game loop
    current_player = 'X'
    for _ in range(9):
        print_board(board)
        row = int(input(f"Player {current_player}, enter the row (0, 1, 2): "))
        col = int(input(f"Player {current_player}, enter the column (0, 1, 2): "))
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

if __name__ == "__main__":
    main()