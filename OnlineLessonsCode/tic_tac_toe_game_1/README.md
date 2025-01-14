# Tic Tac Toe Game

This is a simple Tic Tac Toe game implemented in Python, featuring a computer opponent. Players can take turns playing against each other or against the computer.

## Project Structure

```
tic_tac_toe_game
├── src
│   ├── tic_tac_toe.py       # Main game logic
│   └── computer_opponent.py  # Logic for the computer opponent
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## How to Run the Game

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies by running:
   ```
   pip install -r requirements.txt
   ```
4. Run the game using:
   ```
   python src/tic_tac_toe.py
   ```

## How to Play

- The game is played on a 3x3 grid.
- Players take turns to place their mark (X or O) in an empty cell.
- The first player to align three of their marks horizontally, vertically, or diagonally wins the game.
- If all cells are filled and no player has aligned three marks, the game ends in a draw.

## Computer Opponent

- The computer opponent uses a simple strategy to make its moves.
- It will attempt to block the player from winning while also trying to win itself.

## Dependencies

- This project may require additional libraries for enhanced functionality. Check `requirements.txt` for details.

Enjoy playing Tic Tac Toe!