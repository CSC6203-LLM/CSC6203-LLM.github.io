#!/bin/bash

# Set the paths for input and output files
input_path="./data/1.exam.json"
output_path="./data/2.exam_prepared.jsonl"

# run Python scripts
python 1.prepare_data.py --input_path "$input_path" --output_path "$output_path"
