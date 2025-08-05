import argparse
import json
from get_example_modules import EuclideanDistanceQuestionMaskSelector
from tqdm import tqdm

def get_example_prefix():
    return "### Some example pairs of question and corresponding SQL query are provided based on similar problems:\n"


def format_example(example: dict):
    template_qa = "\n\n### {}\n{}"
    return template_qa.format(example['question'].replace('\n',' ').strip(), example['sql'].replace('\n',' ').strip())




def run_sql_generation(input_data,out_file,k_shot=0,):

    # load_libray
    if k_shot != 0:
        examples_libary = EuclideanDistanceQuestionMaskSelector()
        print(f"k shot: {k_shot}")

    all_prompts = []
    # get all prompts for parallel
    print('Generating ...')
    for i, sample in tqdm(enumerate(input_data)):
        if k_shot != 0:
            examples = examples_libary.get_examples(sample,k_shot)
            answer = "### Some example pairs of question and corresponding SQL query are provided based on similar problems:"
            for example in examples:
                answer += format_example(example)
        
        all_prompts.append(answer)


    with open(out_file, 'w', encoding='utf-8') as file:
        json.dump(all_prompts, file, ensure_ascii=False, indent=4)





if __name__ == '__main__':

    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser()

    # 添加命令行选项

    ## 这里的dataset是ppl_dev.json
    parser.add_argument("--dataset", type=str, default="ppl_dev.json")
    parser.add_argument("--out_file", type=str, default="raw.txt")
    parser.add_argument("--kshot", type=int, default=3)
    # 解析命令行参数
    args = parser.parse_args()

    input_data = json.load(open(args.dataset, 'r'))
    print()

    run_sql_generation( input_data, args.out_file, args.kshot)








