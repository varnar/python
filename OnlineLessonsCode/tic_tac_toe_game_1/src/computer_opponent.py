def get_computer_move(board):
    # Check for a winning move
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = 'O'  # Assume 'O' is the computer
                if check_winner(board):
                    return (row, col)
                board[row][col] = ' '  # Reset the move

    # Block opponent's winning move
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = 'X'  # Assume 'X' is the player
                if check_winner(board):
                    board[row][col] = 'O'  # Block the move
                    return (row, col)
                board[row][col] = ' '  # Reset the move

    # Choose a random available move
    available_moves = [(row, col) for row in range(3) for col in range(3) if board[row][col] == ' ']
    if available_moves:
        return available_moves[0]  # Return the first available move

    return None  # No moves available