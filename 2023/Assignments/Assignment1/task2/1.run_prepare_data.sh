#!/bin/bash

# Set the paths for input and output files
input_path="./data/1.rlhf.jsonl"
output_path="./data/2.rlhf_prepared.jsonl"

# run Python scripts
python 1.prepare_data.py --input_path "$input_path" --output_path "$output_path"
