import random

ROCK = 'r'
PAPER = 'p'
SCISSOR = 's'
ENDGAME = 'q'

emojis = {
    ROCK: 'rock 🪨',
    PAPER: 'paper 📄',
    SCISSOR: 'scissor ✂️',
    ENDGAME: 'End game 🛑'
}
choices = tuple(emojis.keys())

def get_user_choice():
    while True:
        user_choice = input(
            'Rock, paper, scissor or {ENDGAME} for end game (r/p/s): '
            ).lower()
        if user_choice in choices:
            return user_choice
        else: 
            print('Invalid choice!')

def display_choices(user_choice, computer_choice):
    print(f'User choice: {emojis[user_choice]}')
    print(f'Computer choice: {emojis[computer_choice]}')

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        print('It\'s a draw!')
    elif (
        (user_choice == ROCK and computer_choice == SCISSOR) or
        (user_choice == PAPER and computer_choice == ROCK) or
        (user_choice == SCISSOR and computer_choice == PAPER) ):
        print('You win!')
    else: 
        print('You lose!')

while True:
    user_choice = get_user_choice()
    if user_choice == ENDGAME:
        print('End game! {emojis[ENDGAME]}')
        break
    computer_choice = random.choice(choices)

    display_choices(user_choice, computer_choice)
    determine_winner(user_choice, computer_choice) 


