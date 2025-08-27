import json

with open('src/information/ppl_dev.json', 'r') as f:
    ppls = json.load(f)

with open('src/information/augmentation.json', 'r') as f:
    datas = json.load(f)

for i in range(len(datas)):
    data = datas[i]
    ppls[i]['sql_keywords'] = data['sql_keywords']
    ppls[i]['conditions'] = data['conditions']

with open('src/information/ppl_dev.json', 'w') as f:
    json.dump(ppls, f, indent=4, ensure_ascii=False)
