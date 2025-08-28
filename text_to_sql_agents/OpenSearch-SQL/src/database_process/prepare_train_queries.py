import argparse, os,sys,re,tqdm
import pandas as pd
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm.model import model_chose
## model "gpt-4 32K" "gpt-3.5-16K-1106"
## add parse to train.json
# 设置基本配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_table(s, sql):
    l = re.findall(' ([^ ]*) +AS +([^ ]*)', sql)
    for li in l:
        s = s.replace(f" {li[1]}.", f" {li[0]}.")
    return s

def parse_ans(sql,ans):
    ans = ans.replace('```\n','').replace('```','')
    ans = convert_table(ans, sql)
    reason=re.search("#reason:.*",ans).group()
    column=re.search("#columns:.*",ans).group()
    values=re.search("#values:.*",ans).group()
    select=re.search("#SELECT:.*",ans).group()
    sqllike="#SQL-Like:"+re.search("#SQL-[Ll]ike:(.*)",ans).groups()[0]
    final_str="\n".join([reason,column,values,select,sqllike,f"#SQL: {sql}"])
    return final_str

def extract_ans(sql,ans):
    reason=re.search("#reason:.*",ans).group()
    column=re.search("#columns:.*",ans).group()
    vals=re.findall("'((?:''|[^'])*)'",sql)
    vals_f=[f"\"{x}\"" for x in vals if x!="%Y"]
    final_str=f"{reason}\n{column}\n#values: {', '.join(vals_f)}"
    return final_str

def prepare_train_queries(data_dir, new_train_dir, model, start=0, end=9427):
    """
    Prepares training queries from preprocessed data by parsing questions, evidence, and SQL commands using a specified model.

    Args:
        data_dir (str): The directory containing preprocessed data.
        new_train_dir (str): The directory to save the processed training queries.
        model: The model used for parsing the queries.
        start (int, optional): The starting index for processing. Defaults to 0.
        end (int, optional): The ending index for processing. Defaults to 9427.

    Returns:
        None: The function processes the data and saves it to a JSON file.
    """
    
    # Construct the path to the preprocessed training JSON file
    train_json = os.path.join(data_dir, 'data_preprocess', 'train.json')  
    
    # Load the JSON data into a DataFrame
    df = pd.read_json(train_json)
    
    # Iterate over each row of the DataFrame from start to end index
    for i in tqdm.tqdm(range(start, end), total=end - start):    
        for _ in range(3):  # Allow up to 3 attempts for each row
            try:
                # Extract the question, evidence, and SQL command from the DataFrame
                q, e, sql = df.iloc[i]['question'], df.iloc[i]["evidence"], df.iloc[i]["SQL"]
                # Call the model to parse the question and evidence, obtaining the content
                content = model_chose("prepare_train_queries", model).fewshot_parse(q, e, sql)
                # Store the parsed content and extracted answer in the DataFrame
                df.loc[i, 'parse'] = content.strip()+"\n#SQL: "+sql### generate fewshot
                df.loc[i, 'extract'] = extract_ans(sql, content)### extract fewshot
                break  # Exit the retry loop if successful
            except Exception as e:
                # Print an error message if processing fails
                print(f"Error processing row {i}: {str(e)}")  
    
    # Save the processed DataFrame to a new JSON file in the specified directory
    df[start:end].to_json(new_train_dir, orient='records', indent=4)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db_root_directory',
                        type=str,
                        help='data path',
                        default="Bird")
    parser.add_argument('--model',
                        type=str,
                        help='model',
                        default="gpt-4o-mini-0718")
    parser.add_argument('--start',
                        type=int,
                        help='start_point',
                        default=0)
    parser.add_argument('--end',
                        type=int,
                        help='end_point',
                        default=9428)
    args = parser.parse_args()

    logging.info(f"Start generate_fewshot_step_1,the output_file is {args.db_root_directory}/llm_train_parse.json")
    llm_train_json=os.path.join(args.db_root_directory,'llm_train_parse.json')
    prepare_train_queries(args.db_root_directory,llm_train_json,args.model,args.start,args.end)
    

