import pandas as pd
import json
import argparse

file_path = 'few_shot/train-00000-of-00001-fe8894d41b7815be.parquet'


def read_parquet(file_path):
    df = pd.read_parquet(file_path)
    answers = []

    for row in df.iterrows():
        answer = {}
        answer['question'] = row[1]['question']
        answer['sql'] = row[1]['SQL']
        answers.append(answer)

    return answers


def main():
    answers = read_parquet(file_path)

    with open('few_shot/QA.json', 'w') as f:
        json.dump(answers, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':

    main()
