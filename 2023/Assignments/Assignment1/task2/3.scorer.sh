#!/bin/bash

# Define the paths to your input, output, and score files
input_file="./data/3.rlhf_aftgpt.jsonl"
wrong_ans_path="./data/4.wrong_ans.json"
score_file="./data/4.score.json"

python 3.scorer.py --input_path "$input_file" --wrong_ans_path "$wrong_ans_path" --score_path "$score_file"

