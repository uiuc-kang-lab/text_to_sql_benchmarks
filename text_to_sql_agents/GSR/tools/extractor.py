import json
import re

from openai import OpenAI
from run.run_config import model_openai

from .tools_config import FEW_SHOT, KEYWORD_EXTRACT_FEW_SHOT
from run.run_config import API_KEYS

client = OpenAI(
    api_key=API_KEYS)


def text_extractor(pre_message_content):
    input_pattern = r'###Input:\n(.*?)(?:\n###|$)'
    match = re.search(input_pattern, pre_message_content, re.DOTALL)
    return match.group(1).strip() if match else "No match found"


def extractor(pre_sql):

    message = FEW_SHOT + "Input:\n" + pre_sql + "\nOutput:\n"
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model=model_openai,
            temperature=0.2,
            max_tokens=4096
        )
        output_message = response.choices[0].message.content

        return output_message
    except Exception as e:
        print(e)
        return e



def text_keyword_column_value_extractor(text, pre_sql, columns):
    columns_info = ", ".join([f'"{col}"' for col in columns])
    message = KEYWORD_EXTRACT_FEW_SHOT + "Input:" + "\n###Text: " + text + "\n###SQL: " + pre_sql + "\n###Columns: " + columns_info + "\n\n###Ouput:"
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model=model_openai,
            temperature=0.2,
            max_tokens=4096
        )
        output_message = response.choices[0].message.content

        pattern = r'\{.*?\}'

        output_message = re.search(pattern, output_message).group()
        keyword_column_value_dict = json.loads(output_message)

        return keyword_column_value_dict
    except Exception as e:
        print(e)
        return e