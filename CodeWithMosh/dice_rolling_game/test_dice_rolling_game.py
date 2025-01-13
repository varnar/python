import unittest
from unittest.mock import patch
from io import StringIO
import random
import dice_rolling_game

class TestDiceRollingGame(unittest.TestCase):
    @patch('builtins.input', side_effect=['y', 'n'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_roll_dice_yes_then_no(self, mock_stdout, mock_input):
        with patch('random.randint', side_effect=[3, 5]):
            dice_rolling_game.main()
            self.assertIn("You rolled a 3,5", mock_stdout.getvalue())
            self.assertIn("Thank you for playing!", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['n'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_roll_dice_no(self, mock_stdout, mock_input):
        dice_rolling_game.main()
        self.assertIn("Thank you for playing!", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['invalid', 'n'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_input(self, mock_stdout, mock_input):
        dice_rolling_game.main()
        self.assertIn("Invalid input. Please enter 'y' or 'n'.", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
