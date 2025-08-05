import json


with open('sql.txt', 'r') as f:
    datas = f.readlines()
with open('../data/dev.json', 'r') as f:
    ppls = json.load(f)

all={}

for i in range(len(datas)):
    sql = datas[i].strip()
    db = ppls[i]['db_id'].strip()
    sql = sql+';\t----- bird -----\t'+db

    all[f"{i}"]=sql

with open('predict_dev.json','w') as f:
    json.dump(all,f,indent=4,ensure_ascii=False)














