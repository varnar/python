def validate_input(user_input):
    if user_input in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        return True
    return False

def display_message(message):
    print(message)