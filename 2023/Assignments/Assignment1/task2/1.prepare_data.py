import jsonlines
import json
import argparse

prompt = '''
[Question]:
{question}

[Answer1]:
{answer1}

[Answer2]:
{answer2}

A good response should be relevant, accurate and helpful. Which is better, Answer1 or Answer2?
Do not explain your answer, just output 'Answer1' or 'Answer2'.
'''

def generate_query(data):
    chatgpt_query = prompt
    chatgpt_query = chatgpt_query.format_map({'question':data['Question'],'answer1':data['Answer1'],'answer2':data['Answer2']})
    return chatgpt_query


def Prepare_data(args):
    data = []
    # 读取上传的JSONl文件
    with jsonlines.open(args.input_path, "r") as reader:
        data=list(reader)

    print(f"len:{len(data)}")
    # 根据要求转换
    jsonl_data = []


    for id, item in enumerate(data):
        jsonl_data.append(
            {
                "id":id,
                "query": generate_query(item),
                "model_answer": "",
                "groundtruth": item['Preference']
            }
        )

    # 将转换后的数据保存为JSONL文件
    with open(args.output_path, "w", encoding="utf-8") as file:
        for entry in jsonl_data:
            file.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    print(f"Prepare finished, output to '{args.output_path}'")
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Prepare data for OpenAIGPT generation")
    parser.add_argument("--input_path", type=str, required=True, help="Path to the input JSON file.")
    parser.add_argument("--output_path", type=str, required=True, help="Path to the output JSONL file.")
    args = parser.parse_args()
    Prepare_data(args)
