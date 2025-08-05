import json
from tqdm import tqdm
from utils.db_op import get_table_infos, get_foreign_key_infos, get_throw_row_data
import os
from configs.config import dev_json_path


def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def generate_db_list(ppls):
    db_list = []
    for ppl in tqdm(ppls):
        db_name = ppl['db_id']
        if db_name not in db_list:
            db_list.append(db_name)
    return db_list


def generate_table_infos(db_list):
    table_str_list = []
    for table in tqdm(db_list):
        table_str = get_table_infos(table)
        table_str_list.append(table_str)
        print(table_str)
        print('-------------------' * 10)
    return table_str_list


def create_output_structure(ppls, table_infos):
    outputs = []
    for i in tqdm(range(len(ppls))):
        ppl = ppls[i]
        evidence = ppl['evidence']
        db_name = ppl['db_id']
        question = ppl['question']
        # SQL = ppl['SQL']
        foreign_str = get_foreign_key_infos(db_name)

        table_str = next((info['simplified_ddl'] for info in table_infos if info['db'] == db_name), None)
        ddl_data = "#\n" + get_throw_row_data(db_name).strip() + "\n# "

        output = {
            'db': db_name,
            'question': question,
            'simplified_ddl': table_str,
            'ddl_data': ddl_data,
            'evidence': evidence,
            'foreign_key': foreign_str
        }
        outputs.append(output)
    return outputs


def generate_ppl_dev_json(dev_file, out_file):
    ppls = load_json(dev_file)
    db_list = generate_db_list(ppls)
    table_str_list = generate_table_infos(db_list)

    all_table_info = [{'db': db_list[i], 'simplified_ddl': table_str_list[i]} for i in range(len(db_list))]
    save_json(all_table_info, 'src/information/describle.json')

    table_infos = load_json('src/information/describle.json')
    outputs = create_output_structure(ppls, table_infos)

    save_json(outputs, out_file)

    os.remove('src/information/describle.json')


generate_ppl_dev_json(dev_json_path, 'src/information/ppl_dev.json')
