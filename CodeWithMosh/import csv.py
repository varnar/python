import csv

def read_and_print_matching_records(file_path, keyword):
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:  # Added encoding parameter
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if keyword.lower() in row.get('greeting', '').lower():  # Added case-insensitive search
                print(row)

# Example usage
file_path = 'your_file.csv'
keyword = 'hello'
read_and_print_matching_records(file_path, keyword)

import csv

def read_and_print_column_names(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        column_names = csvreader.fieldnames
        print("Column names:", column_names)

# Example usage
file_path = 'your_file.csv'
read_and_print_column_names(file_path)