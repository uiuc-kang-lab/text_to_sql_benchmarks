import openai
import json
from configs.config import api, base_url, model


class GPT:
    def __init__(self):
        self.client = openai.OpenAI(api_key=api, base_url=base_url)

    def __call__(self, instruction, prompt):
        num = 0
        flag = True
        while num < 3 and flag:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": instruction},
                        {"role": "user", "content": prompt},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0,
                    stream=False,

                )
            except Exception as e:
                print(e)
                continue
            try:
                json.loads(response.choices[0].message.content)
                flag = False
            except:
                flag = True
                num += 1

        return response.choices[0].message.content
