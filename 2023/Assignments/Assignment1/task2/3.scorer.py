import re
import jsonlines
import json
import argparse
import os

def match_choice(text):
    match = re.findall(r'.*?([A-E]+(?:[、, ]+[A-E]+)*)', text)
    if match:
        last_match = match[-1]
        return ''.join(re.split(r'[、, ]+', last_match))
    return ''

def calculate_score(question_type, groundtruth, model_answer):
    choice = match_choice(model_answer)
    if len(choice) > 1 and question_type != '多项选择题':
        choice = choice[0]
    return choice == groundtruth, choice

def score_result(input_path, wrong_ans_path, score_path):
    items = []

    with jsonlines.open(input_path, "r") as reader:
        items = list(reader)

    correct = 0
    total = 0
    wrong_data=[]
    for item in items:
        if item['model_answer']==item['groundtruth']:
            correct += 1
        else:
            wrong_data.append(item)
        total += 1

    print(f'总分：{correct}  / 满分：{total}')
    print(f'错误分类：{len(wrong_data)}，已输出到 {wrong_ans_path}')
    
    with open(wrong_ans_path, 'w', encoding='utf-8') as fw:
        json.dump(wrong_data, fw, ensure_ascii=False, indent=4)

    # Output scores to a separate file
    preference_answer = [item['model_answer']for item in items]
    score_info = {
        'correct': correct,
        'total': total,
        'num_answer1': preference_answer.count('Answer1'),
        'num_answer2': preference_answer.count('Answer2'),
    }
    
    with open(score_path, 'w', encoding='utf-8') as fscore:
        json.dump(score_info, fscore, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Score and analyze questions.')
    parser.add_argument('--input_path', required=True, help='Path to the input JSON file')
    parser.add_argument('--wrong_ans_path', required=True, help='Path to the output JSON file for incorrect answers')
    parser.add_argument('--score_path', required=True, help='Path to the output JSON file for scores')

    args = parser.parse_args()
    score_result(args.input_path, args.wrong_ans_path, args.score_path)
