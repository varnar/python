import random

number_to_guess = random.randint(1, 100)

while True:
    try:
        user_input = input ("Guess the number between 1 and 100: ")
        guess = int(user_input)
        if guess > number_to_guess:
            print("Guess lower.")
        elif guess < number_to_guess:
            print("Guess higher.")
        else:
            print("You guessed the number!")
            break
    except ValueError:
        print("Please enter a valid number.")
