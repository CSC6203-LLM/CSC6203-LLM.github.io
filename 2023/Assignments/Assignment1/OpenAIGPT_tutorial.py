import openai
import random

# openai.api_base =  "https://openai.huatuogpt.cn/v1"

class OpenAIGPT:
    def __init__(self, model_name="gpt-3.5-turbo", keys_path=None):
        self.model_name = model_name
        with open(keys_path, encoding="utf-8", mode="r") as fr:
            self.keys = [line.strip() for line in fr if len(line.strip()) >= 4]
    
    def call(self):
        current_key = random.choice(self.keys)
        openai.api_key = current_key
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role":"system", "content": "you are a helpful assistant"},
                {"role": "user", "content": "Tell me a fun fact"},
                {"role": "assistant", "content": "Sure, here is an interesting fact:"}
            ],
            temperature=0.6,
            top_p=0.8,
            frequency_penalty=0.6,
            presence_penalty=0.8,
            n=1
        )
        return response
    

if __name__ == '__main__':
    # test code
    igpt=OpenAIGPT(keys_path="gpt3keys.txt")
    answer=igpt.call()
    print(answer)