import random
from termcolor import cprint

QUESTION = 'question'
OPTIONS = 'options'
ANSWER = 'answer'

def ask_question(index, question, options):
    cprint(f"Question {index}: {question}",'yellow')
    for option in options:
        cprint(option,'cyan')
    return input("Enter your answer: ").upper().strip()
    
def run_quiz(quiz):
    random.shuffle(quiz)
    score = 0

    for index,item in enumerate(quiz,1):
        answer = ask_question(index, item[QUESTION], item[OPTIONS])
        if answer == item[ANSWER]:
            cprint("Correct!",'green')
            score += 1
        else:
            cprint(f"Incorrect! The correct answer is {item[ANSWER]}",'red') 
    cprint(f"Your score is {score}/{len(quiz)}",'blue')

def main():
    quiz = [
        {
            QUESTION:"What is the capital of India?",
            OPTIONS:["A. Mumbai", "B. Delhi", "C. Chennai", "D. Kolkata"],
            ANSWER:"B"
        },
        {
            QUESTION:"What is the capital of USA?",
            OPTIONS:["A. New York", "B. Washington D.C.", "C. Los Angeles", "D. Chicago"],
            ANSWER:"B"
        },
        {
            QUESTION:"What is the capital of UK?",
            OPTIONS:["A. Manchester", "B. Birmingham", "C. London", "D. Liverpool"],
            ANSWER:"C"
        },
        {
            QUESTION:"What is the capital of Australia?",
            OPTIONS:["A. Sydney", "B. Melbourne", "C. Canberra", "D. Perth"],
            ANSWER:"C"
        },
        {
            QUESTION:"What is the capital of Japan?",
            OPTIONS:["A. Tokyo", "B. Osaka", "C. Kyoto", "D. Hiroshima"],
            ANSWER:"A"
        }
    ]    
    cprint("Welcome to Quiz Game!",'blue')
    run_quiz(quiz)

if __name__ == "__main__":
    main()