import csv
#IMPORTANT, WE SHOUDL ALSO USE THIS FOR SEC CLEANING
def parse_question_answer_file(file_path):
    questions = []
    answers = []
    #going over each def and term and then appending to their list
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if "~|~" in line:#specifically doing this, since I seperated as ~|~ during the manual data compilation process
                question, answer = line.split("~|~", 1)
                questions.append(question.strip())
                answers.append(answer.strip())
    return questions, answers
def writer_stuff(questions, answers, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Question/Term', 'Answer/Definition'])
        for question, answer in zip(questions, answers):
            writer.writerow([question, answer])

file_path = 'questions_and_answers.txt'
csv_output = 'questions_and_answers.csv'
json_output = 'questions_and_answers.json'
questions, answers = parse_question_answer_file(file_path)
writer_stuff(questions, answers, csv_output)
