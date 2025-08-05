import openai
import json
from configs.config import api, base_url, model

sys_message = '''{table_info}

### Select the best SQL query to answer the  question:
{candidate_sql}

Your answer should be returned by json format.
{
    "sql": "...",# your SQL query
}
'''


class GPT:
    def __init__(self):
        self.client = openai.OpenAI(api_key=api, base_url=base_url)

    def __call__(self, table_info, candidate_sql):
        prompt = sys_message.replace("{table_info}", table_info).replace("{candidate_sql}", candidate_sql)
        num = 0
        flag = True
        while num < 3 and flag:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
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



