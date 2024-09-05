#!/bin/bash

# Set the path to the Python script
python_script="../OpenAIGPT_datagen_multithread.py"

# set parameter
keys_path="../gpt3keys.txt"
input_path="./data/2.exam_prepared.jsonl"
output_path="./data/3.exam_aftgpt.jsonl"
max_workers=50

python "$python_script" --keys_path "$keys_path" --input_path "$input_path" --output_path "$output_path" --max_workers $max_workers
