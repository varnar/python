def roll_dice():
    import random
    return random.randint(1, 6)

def main():
    print("Welcome to the Dice Rolling Game!")
    scores = []
    while True:         
        input("Press Enter to roll the dice...")
        roll = roll_dice()
        print(f"You rolled a {roll}!")
        scores.append(roll)
        
        play_again = input("Do you want to roll again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            break

    print(f"Your total score is: {sum(scores)}")
    print("Thanks for playing!")

if __name__ == "__main__":
    main()