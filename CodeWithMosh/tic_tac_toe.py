# declare board
board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]
def print_board(board):
    print('  R0  R1  R2 ')
    raw_line = '  ---+---+---'
    print(raw_line)
    count = 0
    for row in board:
        print(f'C{count} {row[0]} | {row[1]} | {row[2]}')
        count += 1
        print(raw_line)

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return True
    for column in range(3):
        if board[0][column] == board[1][column] == board[2][column] != ' ':
            return True
    #check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return True
    return False

def main():
    print("Welcome to Tic Tac Toe!")
    print_board(board)

    current_player = 'X'
    while True:
        print(f"Player {current_player}'s turn")
        row = int(input("Enter row number (0, 1, 2): "))
        column = int(input("Enter column number (0, 1, 2): "))  

        if board[row][column] == ' ':  
            board[row][column] = current_player
            print_board(board) 
        else:
            print("This position is already occupied. Try again.")
            continue

        if check_winner(board):
            print(f"Player {current_player} wins!")
            break

        if current_player == 'X':
            current_player = 'O'
        else:
            current_player = 'X'

        if all([cell != ' ' for row in board for cell in row]): 
            print("It's a tie!")
            break

if __name__ == "__main__":
    main()
