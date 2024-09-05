import openai
from retrying import retry
import random

openai.api_base =  "https://openai.huatuogpt.cn/v1"

class OpenAIGPT:
    def __init__(self, model_name="gpt-3.5-turbo", keys_path=None):
        self.model_name = model_name
        with open(keys_path, encoding="utf-8", mode="r") as fr:
            self.keys = [line.strip() for line in fr if len(line.strip()) >= 4]
        
    def __post_process(self, response):
        return response["choices"][0]["message"]["content"]
    
    @retry(wait_fixed=200, stop_max_attempt_number=50)
    def __call__(self, message):
        if message is None or message == "":
            return False, "Your input is empty."
        
        current_key = random.choice(self.keys)
        openai.api_key = current_key
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": message}
            ],
            temperature=0.6,
            top_p=0.8,
            frequency_penalty=0.6,
            presence_penalty=0.8,
            n=1
        )
        return self.__post_process(response)
    

if __name__ == '__main__':
    # test code
    igpt=OpenAIGPT(keys_path="gpt3keys.txt")
    answer=igpt("下面是一道最佳选择题，请先详细分析问题，最后给出选项。\n1. 根据健康中国战略，推进健康中国建设主要遵循的原则不包括（）。\nA. 健康优先\nB. 改⾰创新\nC. 科学发展\nD. 公开透明")
    print(answer)