import random

# Ask: roll the dice?

# if user input is yes
while True:
    user_input = input("Do you want to roll the dice? (y/n): ")
    # if user
    if user_input.lower() == "y":
        # Generate a random number between 1 and 6
        dice_roll1 = random.randint(1, 6)
        deck_roll2 = random.randint(1, 6)
        # Print the number
        print(f"You rolled a {dice_roll1},{deck_roll2}")
        #user_input = input("Do you want to roll the dice? (y/n): ")
    # if user input is no
    elif user_input.lower() == "n":
        # Print the thank you message
        print("Thank you for playing!")
        # terminate the program
        break
    # else
    else:
        # Print invalid input message
        print("Invalid input. Please enter 'y' or 'n'.")
        #user_input = input("Do you want to roll the dice? (yes/no): ")

