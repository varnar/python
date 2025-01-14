class Game:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # Player 'X' starts first

    def start_game(self):
        while True:
            self.display_board()
            if self.current_player == 'X':
                row, col = self.get_player_move()
            else:
                row, col = self.get_computer_move()

            if self.make_move(row, col):
                if self.check_winner():
                    self.display_board()
                    print(f"Player {self.current_player} wins!")
                    break
                elif self.is_board_full():
                    self.display_board()
                    print("It's a tie!")
                    break
                self.switch_player()

    def display_board(self):
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)

    def get_player_move(self):
        while True:
            try:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter column (0-2): "))
                if self.board[row][col] == ' ':
                    return row, col
                else:
                    print("Cell is already taken. Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter numbers between 0 and 2.")

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            return True
        return False

    def check_winner(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != ' ':
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True
        return False

    def is_board_full(self):
        return all(cell != ' ' for row in self.board for cell in row)

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def get_computer_move(self):
        from computer_opponent import get_computer_move
        return get_computer_move(self.board)