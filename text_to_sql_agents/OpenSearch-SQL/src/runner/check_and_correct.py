import os, sqlite3, re, json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor, TimeoutError
import random, time
from func_timeout import func_timeout, FunctionTimedOut



def sql_raw_parse(sql, return_question):
    sql = sql.split('/*')[0].strip().replace('```sql', '').replace('```', '')
    sql = re.sub("```.*?", '', sql)
    # print(sql)
    rwq = None
    if return_question:
        rwq, sql = sql.split('#SQL:')
    else:
        sql = sql.split('#SQL:')[-1]
    if sql.startswith("\"") or sql.startswith("\'"):  #消除"SELECT
        sql = sql[1:-1]
    sql = re.sub('\s+', ' ', sql).strip()
    return sql, rwq


def get_sql(chat_model,
            prompt,
            temp=1.0,
            return_question=False,
            top_p=None,
            n=1,
            single=True):
    sql = chat_model.get_ans(prompt, temp, top_p=top_p, n=n, single=single)
    # print(sql)
    if single:
        return sql_raw_parse(sql, return_question)
    else:
        return [x['message']['content'] for x in sql], ""


def retable(sql):  # 把T1 恢复原状
    table_as = re.findall(' ([^ ]*) +AS +([^ ]*)', sql)
    for x in table_as:
        sql = sql.replace(f"{x[1]}.", f"{x[0]}.")
    return sql


def max_fun_check(sql_retable):
    fun_amb = re.findall("= *\( *SELECT *(MAX|MIN)\((.*?)\) +FROM +(\w+)",
                         sql_retable)
    # fun_amb=[]
    order_amb = set(re.findall("= (\(SELECT .* LIMIT \d\))", sql_retable))
    select_amb = set(
        re.findall("^SELECT[^\(\)]*? ((MIN|MAX)\([^\)]*?\)).*?LIMIT 1",
                   sql_retable))  # selct 错的
    return fun_amb, order_amb, select_amb


def foreign_pick(sql):
    matchs = re.findall("ON\s+(\w+\.\w+)\s*=\s*(\w+\.\w+) ", sql)
    # print('-----------\n',matchs)
    ma_all = [x for y in matchs for x in y]
    return set(ma_all)


def column_pick(sql, db_col, foreign_set):
    matchs = foreign_pick(sql)
    cols = set()  ## table.`column` 所有column格式统一
    col_table = {}
    ans = set()
    sql_select = set(re.findall("SELECT (.*?) FROM ", sql))
    for x in db_col:  #db_col: table.`column`  同名歧义字段导入
        if sql.find(x) != -1:
            cols.add(x)
        table, col = x.split('.')
        col_table.setdefault(col, [])
        col_table[col].append(table)
    for col in cols:  # 对于SQL中所有存在的 table.col
        table, col_name = col.split('.')
        flag = True
        for x in sql_select:
            if x.find(col) != -1:
                flag = False
                break
        if flag and (col in foreign_set or x in matchs):  # 在外键且select里面没有
            continue
        if col_table.get(col_name):
            Ambiguity = []
            for t in col_table[col_name]:
                tbc = f"{t}.{col_name}"
                if tbc != col:
                    Ambiguity.append(tbc)
                # col_t=f"{t}.{col_name}"
                # ans.append(f"{t}.{col_name}: {db_col[col_t]}")
            if len(Ambiguity):
                amb_des = col + ": " + ", ".join(Ambiguity)
                ans.add(amb_des)

    return sorted(list(ans))


def values_pick(vals, sql):
    val_dic = {}
    ans = set()
    try:
        for val in vals:
            val_dic.setdefault(val[1], [])
            val_dic[val[1]].append(val[0])
        for val in val_dic:
            in_sql, not_sql = [], []
            if sql.find(val):
                for x in val_dic[val]:
                    if sql.find(x) != -1:
                        in_sql.append(f"{x} = '{val}'")
                    else:
                        not_sql.append(f"{x} = '{val}'")
            if len(in_sql) and len(not_sql):
                ans.add(f"{', '.join(in_sql)}: {', '.join(not_sql)}")
        return sorted(list(ans))
    except:
        return []


def func_find(sql):
    fun_amb = re.findall("\( *SELECT *(MAX|MIN)\((.*?)\) +FROM +(\w+)", sql)
    fun_str = []
    for fun in fun_amb:
        fuc = fun[0]
        col = fun[1]
        table = fun[2]
        if fuc == "MAX":
            order = "DESC"
        else:
            order = "ASC"
        str_fun = f"(SELECT {fuc}({col}) FROM {table}): ORDER BY {table}.{col} {order} LIMIT 1"
        fun_str.append(str_fun)
    return "\n".join(fun_str)


t1_tabe_value = re.compile(
    "(\w+\.[\w]+) =\s*'([^']+(?:''[^']*)*)'")  #table.column ="value"
t2_tab_val = re.compile(
    "(\w+\.`[^`]*?`) =\s*'([^']+(?:''[^']*)*)'")  #table.`column` ="value"


def filter_sql(b, bx, conn, SQL, chars=""):
    flag = False
    for x in b:
        sql_t = SQL.replace(bx, f"{chars}{x}")
        try:
            df = pd.read_sql_query(sql_t, conn)
        except Exception as e:
            print(e)
            df = []
        if len(df):
            SQL = sql_t
            flag = True
            break

    return SQL, flag


def join_exec(db, bx, al, question, SQL, chat_model):
    flag = False
    with sqlite3.connect(db, timeout=180) as conn:
        if bx.startswith("IN"):
            b = bx[2:].strip(" ()").split(',')
            SQL, flag = filter_sql(b, bx, conn, SQL, chars="= ")
        elif al.find("OR") != -1:
            a = al.split("OR")
            SQL, flag = filter_sql(a, al, conn, SQL)

    return SQL, flag


def gpt_join_corect(SQL, question, chat_model):
    prompt = f"""下面的question对应的SQL错误的使用了JOIN函数,使用了JOIN table AS T ON Ta.column1 = Tb.column2 OR Ta.column1 = Tb.column3或JOIN table AS T ON Ta.column1 IN的JOIN方式,请你只保留 OR之中优先级最高的一组 Ta.column = Tb.column即可.

question:{question}
SQL: {SQL}

请直接给出新的SQL, 不要回复任何其他内容:
#SQL:"""
    SQL = get_sql(chat_model, prompt, 0.0)[0].split("SQL:")[-1]
    return SQL


def select_check(SQL, db_col, chat_model, question):
    select = re.findall("^SELECT.*?\|\| ' ' \|\| .*?FROM", SQL)
    if select:
        # print("soft change concat")
        SQL = SQL.replace("|| ' ' ||", ', ')

    select_amb = re.findall("^SELECT.*? (\w+\.\*).*?FROM", SQL)
    if select_amb:
        prompt = f"""数据库存在以下字段:
{db_col}
现有问题为 {question}
SQL:{SQL}
我们规定视这种不明确的查询为对应的id
现在请你把上面SQL的{select_amb[0]}改为对应的id,请你直接给出SQL, 不要回复任何其他内容:
#SQL:"""
        # print(prompt)
        SQL = get_sql(chat_model, prompt, 0.0)[0].split("SQL:")[-1]
    return SQL


class soft_check:

    def __init__(self,
                 bert_model,
                 chat_model,
                 soft_prompt,
                 correct_dic,
                 correct_prompt,
                 vote_prompt="") -> None:
        self.bert_model = bert_model
        self.chat_model = chat_model
        self.soft_prompt = soft_prompt
        # self.logger = logger
        self.correct_dic = correct_dic
        self.correct_prompt = correct_prompt
        self.vote_prompt = vote_prompt

    def vote_chose(self, SQLs, question):
        all_sql = '\n\n'.join(SQLs)
        prompt = self.vote_prompt.format(question=question, sql=all_sql)
        # print(prompt)
        SQL_vote = get_sql(self.chat_model, prompt, 0.0)[0]
        return SQL_vote

    def soft_correct(self, SQL, question, new_prompt, hint=""):
        soft_p = self.soft_prompt.format(SQL=SQL, question=question, hint=hint)
        soft_SQL = self.chat_model.get_ans(soft_p, 0.0)
        soft_SQL = re.sub("```\w*", "", soft_SQL)
        # print(soft_SQL)
        soft_json = json.loads(soft_SQL)
        # print(soft_json["Judgment"])

        if (soft_json["Judgment"] == False or soft_json["Judgment"]
                == 'False') and soft_json["SQL"] != "":
            SQL = soft_json["SQL"]
            SQL = re.sub('\s+', ' ', SQL).strip()
        elif (soft_json["Judgment"] == False
              or soft_json["Judgment"] == 'False'):
            SQL = get_sql(self.chat_model, new_prompt, 1.0, False)[0]

        return SQL, soft_json["Judgment"]

    def double_check(
            self,
            new_prompt,
            values: list,
            values_final,
            SQL: str,
            question: str,
            new_db_info: str,
            db_col: list,
            db: str,  #db 路径
            hint="") -> str:
        SQL = re.sub("(COUNT)(\([^\(\)]*? THEN 1 ELSE 0.*?\))", r"SUM\2", SQL)

        # SQL, judgment = self.soft_correct(SQL, question, new_prompt,hint)
        sql_retable = retable(SQL)

        SQL = self.values_check(sql_retable, values, values_final, SQL,
                                question, new_db_info, db_col, hint)
        SQL = self.JOIN_error(SQL, question, db)
        SQL = self.func_check(sql_retable, SQL, question)
        SQL = self.func_check2(question, SQL)  #ORDER BY (MIN|MAX).* LIMIT
        SQL = self.time_check(SQL)
        SQL = self.is_not_null(SQL)
        SQL = select_check(SQL, db_col, self.chat_model, question)
        return SQL, True
    def double_check_style_align(
        self,
        SQL: str,
        question: str,
        db_col: list,
        sql_retable:str,
        ) -> str:
        # SQL = re.sub("(COUNT)(\([^\(\)]*? THEN 1 ELSE 0.*?\))", r"SUM\2", SQL)

        # sql_retable = retable(SQL)
        SQL = self.func_check(sql_retable, SQL, question)
        SQL = self.is_not_null(SQL)
        SQL = select_check(SQL, db_col, self.chat_model, question)
        return SQL, True

    def double_check_function_align(
        self,
        SQL: str,
        question: str,
        db: str,  #db 路径
        ) -> str:
        # SQL = re.sub("(COUNT)(\([^\(\)]*? THEN 1 ELSE 0.*?\))", r"SUM\2", SQL)

        SQL = self.JOIN_error(SQL, question, db)
        SQL = self.func_check2(question, SQL)  #ORDER BY (MIN|MAX).* LIMIT
        SQL = self.time_check(SQL)
        return SQL, True
    
    def double_check_agent_align(
        self,
        sql_retable:str,
        values: list,
        values_final,
        SQL: str,
        question: str,
        new_db_info: str,
        db_col: list,
        hint="") -> str:
        # SQL = re.sub("(COUNT)(\([^\(\)]*? THEN 1 ELSE 0.*?\))", r"SUM\2", SQL)
        # # SQL, judgment = self.soft_correct(SQL, question, new_prompt,hint)
        # sql_retable = retable(SQL)
        SQL = self.values_check(sql_retable, values, values_final, SQL,
                                question, new_db_info, db_col, hint)
        return SQL, True
    
    def JOIN_error(self, SQL, question, db):
        join_mutil = re.findall(
            "JOIN\s+\w+(\s+AS\s+\w+){0,1}\s+ON(\s+\w+\.\w+\s*(=\s*\w+\.\w+(?:\s+OR\s+\w+\.\w+\s*=\s*\w+\.\w+)+|IN\s+\(.*?\)))",
            SQL)
        flag = False
        if join_mutil:
            _, al, bx = join_mutil[0]

            try:
                SQL, flag = func_timeout(180 * 8,
                                         join_exec,
                                         args=(db, bx, al, question, SQL,
                                               self.chat_model))
                # print("soft change JOIN")
            except FunctionTimedOut:
                print("time out join")
            except Exception as e:
                print(e)
        if not flag and join_mutil:  ##没改正
            SQL = gpt_join_corect(SQL, question, self.chat_model)
            print("soft change JOIN gpt")

        return SQL

    def is_not_null(self, SQL):
        SQL = SQL.strip()
        # print(SQL)
        inn = re.findall("ORDER BY .*?(?<!DESC )LIMIT +\d+;{0,1}", SQL)
        if not inn:
            return SQL
        for x in inn:
            if re.findall("SUM\(|COUNT\(", x):
                return SQL
        prompt = f"""请你为下面SQL ORDER BY的条件加上WHERE IS NOT NULL限制:
SQL:{SQL}

请直接给出新的SQL, 不要回复任何其他内容:
#SQL:"""
        # print("soft change IS NOT NULL")
        SQL = get_sql(self.chat_model, prompt, 0.0)[0].split("SQL:")[-1]
        return SQL

    def time_check(self, sql):
        time_error_fix = re.sub("(strftime *\([^\(]*?\) *[>=<]+ *)(\d{4,})",
                                r"\1'\2'", sql)
        # if sql != time_error_fix:
        #     print("soft change 3 time")
        return time_error_fix

    def func_check2(self, question, SQL):
        res = re.search("ORDER BY ((MIN|MAX)\((.*?)\)).*? LIMIT \d+", SQL)
        if res:
            prompt = f"""对于下面的qustion和SQL:
#question: {question}
#SQL: {SQL}

ERROR: {res.group()} 是一种不正确的用法, 请对SQL进行修正, 注意如果SQL中存在GROUP BY, 请判断{res.groups()[0]}的内容是否需要使用 SUM({res.groups()[2]})

请直接给出新的SQL, 不要回复任何其他内容:"""
            # print(prompt)
            # print("soft change func 2")
            SQL = get_sql(self.chat_model, prompt, 0.1)[0]
        return SQL

    def func_check(self, sql_retable, sql, question):
        fun_amb, order_amb, select_amb = max_fun_check(sql_retable)
        if not fun_amb and not order_amb and not select_amb:
            return sql
        fun_str = []
        origin_f = []
        for fun in fun_amb:
            fuc = fun[0]
            col = fun[1]
            table = fun[2]
            if fuc == "MAX":
                order = "DESC"
            else:
                order = "ASC"
            str_fun = f"WHERE {col} = (SELECT {fuc}({col}) FROM {table}): 请用 ORDER BY {table}.{col} {order} LIMIT 1 代替嵌套SQL"
            origin_f.append(
                f"WHERE {col} = (SELECT {fuc}({col}) FROM {table})")
            fun_str.append(str_fun)

        for fun in order_amb:
            origin_f.append(fun)
            fun_str.append(f"{fun}: 使用JOIN 形式代替嵌套")
        for fun in select_amb:
            origin_f.append(fun[0])
            fun_str.append(f"{fun[0]}: {fun[1]} function 函数 冗余,请更改")

        func_amb = "\n".join(fun_str)
        prompt = f"""对于下面的问题和SQL, 请根据ERROR和#change ambuity修改:
#question: {question}
#SQL: {sql}
ERROR:{",".join(origin_f)} 不符合要求, 请使用 JOIN ORDER BY LIMIT 形式代替
#change ambuity: {func_amb}

请直接给出新的SQL, 不要回复任何其他内容:"""
        # print("------\nsoft change func")
        # print(prompt)
        sql = get_sql(self.chat_model, prompt, 0.0)[0]
        # print(sql)
        return sql

    def values_check(self,
                     sql_retable,
                     values,
                     values_final,
                     sql,
                     question,
                     new_db_info,
                     db_col,
                     hint=""):
        # print(sql_retable)
        dic_v = {}
        dic_c = {}
        l_v = list(set([x[1] for x in values]))
        tables = "( " + " | ".join(set([x.split(".")[0]
                                        for x in db_col])) + " )"
        for x in values:
            dic_v.setdefault(x[1], [])
            dic_v[x[1]].append(x[0])
            dic_c.setdefault(x[0], [])
            dic_c[x[0]].append(x[1])
        value_sql = re.findall(t1_tabe_value,
                               sql_retable)  # find all = "value"
        value_sql.extend(re.findall(t2_tab_val, sql_retable))
        tabs = set(re.findall(tables, sql))
        if len(tabs) == 1:  #单表
            val_single = re.findall("[ \(]([\w]+) =\s*'([^']+(?:''[^']*)*)'",
                                    sql)
            val_single.extend(
                re.findall("[ \(]([\w]+) =\s*'([^']+(?:''[^']*)*)'", sql))
            val_single = set(val_single)
            tab = tabs.pop()[1:-1]
            for x in val_single:
                value_sql.append((f"{tab}.{x[0]}", x[1]))
        # print(value_sql, dic_v)
        badval_l = []
        change_val = []
        value_sql = set(value_sql)
        for tab_val in value_sql:
            tab, val = tab_val
            if len(re.findall("\d", val)) / len(val) > 0.6:
                continue
            # print(val, l_v)
            tmp_col = dic_v.get(val)
            if not tmp_col and len(l_v):  ## 值错了但非常接近
                # print(val, l_v)
                val_close = self.bert_model.encode(
                    val, show_progress_bar=False) @ self.bert_model.encode(
                        l_v,
                        show_progress_bar=False,
                    ).T
                if val_close.max() > 0.95:
                    val_new = l_v[val_close.argmax()]
                    sql = sql.replace(f"'{val}'", f"'{val_new}'")
                    val = val_new
                    # print("soft change 1 similar values")

            tmp_col = dic_v.get(val)
            tmp_val = dic_c.get(tab, {})
            if tmp_col and tab not in tmp_col:  #数据库中存在了val但table不对 以及值完全错
                lt = [f"{x} ='{val}'" for x in tmp_col]
                lt.extend([f"{x} ='{val}'" for x in tmp_val])
                rep = ", ".join(lt)
                badval_l.append(f"{tab} = '{val}'")
                # print(rep)
                change_val.append(f"{tab} = '{val}': {rep}")

        if badval_l:
            v_l = "\n".join(change_val)
            prompt = f"""Database Schema:
{new_db_info}

#question: {question}
#SQL: {sql}
ERROR: 数据库中不存在: {', '.join(badval_l)}
请用以下条件重写SQL:\n{v_l}

请直接给出新的SQL,不要回复任何其他内容:
#SQL:"""
            # print("------\nsoft change 2 val not exists")
            # print(prompt)
            sql = get_sql(self.chat_model, prompt, 0.0)[0]
            # print(sql)
        return sql

    def correct_sql(self,
                    db_sqlite_path,
                    sql,
                    query,
                    db_info,
                    hint,
                    key_col_des,
                    new_prompt,
                    db_col={},
                    foreign_set={},
                    L_values=[]):
        # db = os.path.join(DB_dir, db, db + ".sqlite")

        conn = sqlite3.connect(db_sqlite_path, timeout=180)
        count = 0
        raw = sql
        none_case = False
        while count <= 3:
            try:
                # def
                # ans,time_cost=func_timeout(180,sql_exec,args=(SQL,dbt))
                df = pd.read_sql_query(sql, conn)
                if len(df) == 0:
                    raise ValueError("Error':Result: None")
                else:
                    break
            except Exception as e:
                if count >= 3:  #重新生成一次SQL
                    wsql = sql
                    sql = get_sql(self.chat_model, new_prompt, 0.2)[0]
                    # self.logger.info("correct 失败:\n%s\n regen sql:%s", wsql,
                    #                  sql)
                    none_case = True
                    break
                count += 1
                tag = str(e)
                e_s = str(e).split("':")[-1]
                result_info = f"{sql}\nError: {e_s}"
            if sql.find("SELECT") == -1:
                sql = get_sql(self.chat_model, new_prompt, 0.3)[0]
            else:
                fewshot = self.correct_dic["default"]
                advice = ""

                for x in self.correct_dic:
                    if tag.find(x) != -1:  #找到了错误原因就不往下找了
                        # print(tag)
                        fewshot = self.correct_dic[x]
                        if e_s == "Result: None":
                            sql_re = retable(sql)
                            adv = column_pick(sql_re, db_col, foreign_set)
                            adv = '\n'.join(adv)
                            val_advs = values_pick(L_values, sql_re)
                            val_advs = '\n'.join(val_advs)
                            func_call = func_find(sql)
                            if len(adv) or len(val_advs) or len(func_call):
                                advice = "#Change Ambiguity: " + "(replace or add)\n"
                                l = [
                                    x for x in [adv, val_advs, func_call]
                                    if len(x)
                                ]
                                advice += "\n\n".join(l)
                        elif x == "no such column":
                            advice += "Please check if this column exists in other tables"
                        break
                fewshot=""
                advice=""
                cor_prompt = self.correct_prompt.format(
                    fewshot=fewshot,
                    db_info=db_info,
                    key_col_des=key_col_des,
                    q=query,
                    hint=hint,
                    result_info=result_info,
                    advice=advice)
                # self.logger.info("cor_prompt:\n%s", cor_prompt)
                sql = get_sql(self.chat_model,
                              cor_prompt,
                              0.2 + count / 5,
                              top_p=0.3)[0]
                # print(sql)
            # self.logger.info("cor_sql:\n%s", sql)

            raw = sql

        conn.close()
        return sql, none_case



def sql_exec(SQL, db):
    with sqlite3.connect(db) as conn:
        s = time.time()
        df = pd.read_sql_query(SQL, conn)
        ans = set(tuple(x) for x in df.values)
        time_cost = time.time() - s
    return ans, time_cost

def get_sql_ans(SQL,db_sqlite_path):
    try:
            # dbt = os.path.join(DB_dir, db, db + ".sqlite")
        ans, time_cost = func_timeout(180, sql_exec, args=(SQL, db_sqlite_path))
    except FunctionTimedOut:
        ans,time_cost=[],100000
        print("time out")
    except Exception as e:
        ans,time_cost=[],100000
        print(f"SQL execution error: {e}")
    return ans,time_cost
    
def process_sql(Dcheck, SQL,L_values, values, question,
                new_db_info, db_col_keys, hint,key_col_des,tmp_prompt,db_col,foreign_set,align_methods,db_sqlite_path):
    node_names=align_methods.split('+')
    # print(node_names)
    align_functions = {
        "agent_align": Dcheck.double_check_agent_align,
        "style_align": Dcheck.double_check_style_align,
        "function_align": Dcheck.double_check_function_align
    }
    SQL = re.sub("(COUNT)(\([^\(\)]*? THEN 1 ELSE 0.*?\))", r"SUM\2", SQL)
    sql_retable = retable(SQL)
    judgment = None
    sql_history={}
    SQL_correct=SQL
    for node_name in node_names:
        if node_name in align_functions:
            # 根据不同的环节调用对应的方法
            if node_name == "agent_align":
                SQL, judgment = align_functions[node_name](sql_retable, L_values, values, SQL,
                                                           question, new_db_info, db_col_keys, hint)
            elif node_name == "style_align":
                SQL, judgment = align_functions[node_name](SQL, question, db_col_keys,sql_retable)
            elif node_name == "function_align":
                SQL, judgment = align_functions[node_name](SQL,question,db_sqlite_path)
            sql_history[node_name]=SQL
    align_SQL=SQL
    can_ex = True
    nocse = True
    ans = set()
    time_cost = 10000000


    try:
        SQL, nocse = func_timeout(540,
                                  Dcheck.correct_sql,
                                  args=(db_sqlite_path, SQL, question, new_db_info,
                                        hint, key_col_des, tmp_prompt, db_col,
                                        foreign_set, L_values))
    except:
        print("timeout")
        can_ex = False

    if can_ex:
        ans,time_cost=get_sql_ans(SQL, db_sqlite_path)
        # align_ans=get_sql_ans(align_SQL, db_sqlite_path)
        # correct_ans=get_sql_ans(SQL_correct, db_sqlite_path)
        align_ans=None
        correct_ans=None
    return sql_history,SQL,ans,nocse,time_cost,align_SQL,align_ans,SQL_correct,correct_ans

def muti_process_sql(Dcheck, SQLs, L_values, values, question,
                     new_db_info, hint,key_col_des,tmp_prompt,db_col,foreign_set,align_methods,db_sqlite_path,n):
    vote = []
    none_case = False

    db_col_keys=db_col.keys()
    # Use ThreadPoolExecutor to execute the process_sql function concurrently
    with ThreadPoolExecutor(max_workers=n) as executor:
        # Submit all tasks

        future_to_sql = {
            executor.submit(process_sql, Dcheck, SQL, L_values, values, question, new_db_info, db_col_keys, hint,key_col_des,tmp_prompt,db_col,foreign_set, align_methods, db_sqlite_path): 
            (SQLs[SQL], SQL)
            for SQL in SQLs
        }
        # Collect results as they complete
        time_cost = 10000000
        for future in as_completed(future_to_sql):
            count, tmp_SQL = future_to_sql[future]
            try:
                sql_history, SQL, ans, none_c, time_cost, align_SQL,align_ans,SQL_correct,correct_ans = future.result(timeout=700)
                
                # 将结果添加到 vote
                vote.append({
                    "sql_history": sql_history,
                    "sql": SQL,
                    "answer": ans,
                    "count": count,
                    "time_cost": time_cost,
                    "align_sql":align_SQL,
                    "align_ans":align_ans,
                    "correct_sql":SQL_correct,
                    "correct_ans":correct_ans
                })
                
                none_case = none_case or none_c
            except FunctionTimedOut:
                print(f"Error: Processing SQL timeout for SQL count {count}")
                # 将集合转换为列表
                vote.append({
                    "sql_history": tmp_SQL,
                    "sql": tmp_SQL,
                    "answer": [],  # 使用空列表代替集合
                    "count": 1,
                    "time_cost": time_cost,
                    "align_sql":tmp_SQL,
                    "correct_sql":tmp_SQL,
                    "align_ans":[],
                    "correct_ans":[],
                })
                
                none_case = True
            except Exception as e:
                print(f"Error processing SQL: {e}")
                
                # 将集合转换为列表
                vote.append({
                    "sql_history": tmp_SQL,
                    "sql": tmp_SQL,
                    "answer": [],  # 使用空列表代替集合
                    "count": 1,
                    "time_cost": time_cost,
                    "align_sql":tmp_SQL,
                    "correct_sql":tmp_SQL,
                    "align_ans":[],
                    "correct_ans":[],
                })
                
                none_case = True
    return vote, none_case


