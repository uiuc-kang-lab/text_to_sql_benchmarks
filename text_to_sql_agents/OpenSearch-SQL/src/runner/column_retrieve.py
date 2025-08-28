import pandas as pd
import re
import torch

class ColumnRetriever:
    def __init__(self, bert_model, tables_info_dir):
        self.bert_model = bert_model
        self.tables_info_dir = tables_info_dir

    def get_col_retrieve(self, q, db, l):
        ext_a = list(self.get_kgram(q))
        recall_l = set(re.findall("who|which|where|when", q, re.IGNORECASE))
        recall_dic={"who":["name"],"which":["name","location","id","date","time"],"when":["time","date"],"where":["country","place","location","city"]}
        for x in recall_l:
            ext_a.extend(recall_dic[x.lower()])  # 对应 name
        
        # l = list(df[db].values[1].keys())
        table_dic = self.get_tab_col_dic(l)  # 所有的列名不含表前缀
        l = list(table_dic.keys())
        all_col = self.col_ret(l,ext_a)  # 正式的列名
        
        tab_df = pd.read_json(self.tables_info_dir)
        col_name_d = self.col_name_dic(tab_df, db)
        
        re_col = []
        if col_name_d:
            col_l = list(col_name_d.keys())
            re_col= self.col_ret(col_l,ext_a)  # 非正式列名
        
        ans = self.get_col_set(all_col, re_col, col_name_d, table_dic)
        
        return ans

    def get_kgram(self,q, k=5):
        q = re.sub(r'[^\s\w]', ' ', q)
        q = re.sub(r'\s+', ' ', q)
        q_l = q.split(' ')
        s = set()
        for i in range(1, k):
            for j in range(len(q_l) - i + 1):
                s.add(" ".join(q_l[j:i + j]))
        return s


    def get_tab_col_dic(self,table_list):
        tab_dic = {}
        for x in table_list:
            t, col = x.split(".")
            col = col.strip('`')
            tab_dic.setdefault(col, set())
            tab_dic[col].add(x)

        return tab_dic
    
    def col_ret(self,l,ext_a):
        l_emb = self.bert_model.encode(l,
                                convert_to_tensor=True,
                                show_progress_bar=False)
        num_pick = min(4, len(l))
        m_ans = self.bert_model.encode(
            ext_a, convert_to_tensor=True, show_progress_bar=False) @ l_emb.T
        all_col = self.same_pick(l,m_ans,num_pick)
        return all_col

    def col_name_dic(self,df,db):
        a,b=df[df["db_id"]==db][["column_names","column_names_original"]].values[0]
        return {x[1]:y[1] for x,y in zip(a[1:],b[1:]) if  x[1]!=y[1]}

    def get_col_set(self,all_col,re_col,col_name_d,table_dic,reflect=False):
        ans = set()
        if reflect:

            for x in all_col:
                if x.find(" ")!= -1:
                    x=f"`{x}`"
                ans.add(x)
            for x in re_col:
                tmp=col_name_d[x]
                if tmp.find(" ")!=-1:
                    tmp=f"`{tmp}`"
                ans.add(tmp)
            return ans
        for x in all_col:
            ans = ans.union(table_dic[x])
        
        for x in re_col:
            real_name=col_name_d[x]
            if real_name not in all_col:
                ans = ans.union(table_dic[real_name])
        return ans

    def same_pick(self,l,m_ans,num_pick,shold=0.7):
        all_col = set((torch.topk(
            m_ans,
            num_pick).indices[torch.topk(m_ans, num_pick).values > shold]).tolist())
        all_col=set(l[x] for x in all_col)
        return all_col


