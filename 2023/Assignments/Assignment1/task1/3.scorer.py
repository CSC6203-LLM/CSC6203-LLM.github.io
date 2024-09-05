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

    question_type = ['最佳选择题', '配伍选择题', '综合分析选择题', '多项选择题']
    type2score = {q_type: {'correct': 0, 'total': 0} for q_type in question_type}
    wrong_data = []

    for item in items:
        q_type = item['question_type']
        groundtruth = item['groundtruth']
        is_correct, model_choice = calculate_score(q_type, groundtruth, item['model_answer'])

        if is_correct:
            type2score[q_type]['correct'] += 1
        else:
            item['model_choice'] = model_choice
            wrong_data.append(item)

        type2score[q_type]['total'] += 1

    total_correct = 0
    for q_type, item in type2score.items():
        sub_total = item['total']
        if sub_total == 0:
            continue
        total_correct = total_correct + item['correct']
        accuracy = item['correct'] / item['total']
        print(f'[{q_type}]准确率：{accuracy:.3f}  题目总数：{sub_total}')

    total_questions = len(items)
    print(f'总分：{total_correct}  / 满分：{total_questions}')
    print(f'错误题目：{len(wrong_data)}道，已输出到 {wrong_ans_path}')
    
    with open(wrong_ans_path, 'w', encoding='utf-8') as fw:
        json.dump(wrong_data, fw, ensure_ascii=False, indent=4)

    # Output scores to a separate file
    score_info = {
        'total_score': total_correct,
        'total_questions': total_questions,
        'scores_by_type': type2score
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
