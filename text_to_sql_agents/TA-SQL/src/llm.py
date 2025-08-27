import time
from tqdm import tqdm
from openai import OpenAI

def connect_gpt4(message, prompt):
    response = OpenAI().chat.completions.create(
                    model="gpt-4o",
                    messages = [{"role":"system","content":f"{message}"}, #"You are a helpful assisant. Help the user to complete SQL and no explaination is needed."
                                {"role":"user", "content":f"{prompt}"}],
                    temperature=0,
                    max_tokens=800, #800
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop = None)
    return response.choices[0].message.content

def collect_response(prompt, max_tokens = 800, stop = None):
    while 1:
            flag = 0
            try:
                response = OpenAI().chat.completions.create(
                    model="gpt-4o",
                    messages = [{"role":"system","content":"You are an AI assistant that helps people find information."}, #"You are a helpful assisant. Help the user to complete SQL and no explaination is needed."
                                {"role":"user", "content":f"{prompt}"}],
                    temperature=0,
                    max_tokens=max_tokens, #800
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop = stop)
                response = response.choices[0].message.content
                flag = 1
                
            except Exception as e:
                print(e)
                time.sleep(1)
            if flag == 1:
                break
    return response
