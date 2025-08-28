import re, json
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

class DES:

    def __init__(self, bert_model, DB_emb, col_values) -> None:
        self.model = bert_model
        self.DB_emb = DB_emb
        self.col_values = col_values

    def get_examples(self, target, topk=3):
        target_embedding = self.model.encode(target,
                                             show_progress_bar=False,
                                            )

        # find the most similar question in train dataset
        all_pair = []
        for key in self.DB_emb:
            embs = self.DB_emb[key]

            distances = np.squeeze(euclidean_distances(target_embedding,
                                                       embs)).tolist()
            distances = [distances] if np.isscalar(distances) else distances
            pairs = [
                (distance, index, key)
                for distance, index in zip(distances, range(len(distances)))
            ]

            pairs_sorted = sorted(pairs, key=lambda x: x[0])

            all_pair.extend(pairs_sorted[:topk])
            all_pair.sort(key=lambda x: x[0])
        return all_pair[:topk]

    def get_key_col_des_single(self, value, topk, debug, des, value_cols,
                               shold, match_filter):

        if len(value) == 0:
            return
        col_key_inst = self.get_examples([value], topk)
        self.logger.info(
            "value\n %s",
            f"{value} {self.col_values[col_key_inst[0][2]][col_key_inst[0][1]]}"
        )

        if debug:
            for x in col_key_inst:
                print(self.col_values[x[2]][x[1]], x[0])
        val_col = []
        matchs = set()
        col_key_inst = same_str_sort(col_key_inst, self.col_values, value)[:5]
        maxm_score = col_key_inst[0][1]
        same = col_key_inst[0][0]
        self.logger.info("col_key_inst\n %s", col_key_inst)

        for match in col_key_inst:
            if (same == match[0] or match[3].lower() == value.lower()
                ) and match[1] < shold and match[
                    2] not in matchs and match[1] - maxm_score < match_filter:

                tab, col = match[2].split('.')
                coll = tab + '.' + quote_field(col)

                val_col.append(f"{coll} = '{match[3]}'")
                value_cols.append(coll)
                matchs.add(match[2])
            else:
                continue
        if val_col:
            val_des = f"'{value}': " + ', '.join(val_col)
            des.append(val_des)

class DES_new(DES):

    def __init__(self, bert_model, DB_emb, col_values) -> None:
        super().__init__(bert_model, DB_emb, col_values)
        self.jump_l = {
            "how", "not", "what", "who", "which", "refer", "from", "with",
            "was", "were", "the", "and", "have", "many", "much", "list", "did"
        }

    def get_key_col_des(self,
                        cols,
                        values,
                        shold=0.8,
                        debug=False,
                        topk=7,
                        match_filter=0.3):
        des = []
        value_cols = []
        for value in values:
            value = value.strip(" '\"")
            if len(value) == 0 or re.fullmatch("\d+\.?\d*", value):
                continue
            self.get_key_col_des_single(value, topk, debug, des, value_cols,
                                        shold, match_filter)
            value_split = value.split(' ')
            if len(value_split) > 1:
                tmp_des = []
                tmp_value_cols = []
                for val in value_split:
                    if val == '':
                        continue
                    val = val.strip()
                    self.get_key_col_des_single(val, topk, debug, tmp_des,
                                                tmp_value_cols,
                                                max(shold / 2,
                                                    0.2), match_filter)
                if len(tmp_des) >= len(value_split):
                    des.extend(tmp_des)
                    value_cols.extend(tmp_value_cols)
        # for value in values_ret:
        #     value = value.strip(" '\"")

            if len(value) < 3 or re.fullmatch(
                    "\d+\.?\d*",
                    value) or value in values or value.lower() in self.jump_l:
                continue
            self.get_key_col_des_single(value,
                                        topk,
                                        debug,
                                        des,
                                        value_cols,
                                        shold,
                                        match_filter,
                                        tag=3,
                                        lcs=True)
        des = sorted(list(set(des)))  #keep order and unique
        # cols = col.split(',')
        cols = cols.union(set(value_cols))

        return cols, des

    def get_key_col_des_single(self,
                               value,
                               topk,
                               debug,
                               des,
                               value_cols,
                               shold,
                               match_filter,
                               tag=10,
                               lcs=False):

        if len(value) == 0:
            return
        col_key_inst = self.get_examples([value], topk)
        # self.logger.info(
        #     "value\n %s",
        #     f"{value} {self.col_values[col_key_inst[0][2]][col_key_inst[0][1]]}"
        # )

        val_col = []
        matchs = set()
        col_key_inst = same_str_sort(col_key_inst, self.col_values,
                                     value)[:topk]
        # print(value,col_key_inst)
        maxm_score = col_key_inst[0][1]
        same = col_key_inst[0][0]
        # self.logger.info("col_key_inst\n %s", col_key_inst)
        val_len = len(value)
        for match in col_key_inst:
            tab, col = match[2].split('.')
            if tab == "sqlite_sequence" or re.fullmatch(
                    "\d+\.?\d*",
                    match[3]) or abs(val_len - len(match[3])) > tag:
                continue
            if (same == match[0] or match[3].lower() == value.lower()
                ) and match[1] < shold and match[
                    2] not in matchs and match[1] - maxm_score < match_filter:

                coll = tab + '.' + quote_field(col)
                # if coll in cols:
                val_ans = match[3].replace("'", "''")
                val_col.append((coll, val_ans))
                value_cols.append(coll)
                matchs.add(match[2])
            else:
                continue
        if debug:
            print(value)
            print(col_key_inst)
            print(val_col)
        if val_col:
            # val_des = f"'{value}': " + ', '.join(val_col)
            # val_des = ', ' .join(val_col)
            des.extend(val_col)


def quote_field(field_name):
    # 正则表达式判断字段名是否包含空格或特殊字符
    if re.search(r'\W', field_name):
        # 如果匹配到，给字段名添加反引号
        return f"`{field_name}`"
    else:
        # 否则，不做改变
        return field_name


def col_update(cols_tmp, db_col):
    col_table = {}
    for x in db_col:  #db_col: table.`column`  同名歧义字段导入
        table, col = x.split('.')
        col_table.setdefault(col, [])
        col_table[col].append(table)
    cols = []  ## table.`column` 所有column格式统一
    for c in cols_tmp:  ##
        try:
            table, col_name = c.split('.')
            col_name = col_name.replace('`', '')
            col_name = quote_field(col_name)
            for t in col_table[col_name]:
                cols.append(f"{t}.{col_name}")  # 都变成 table.`xxx`
        except:
            pass

    return set(cols)


def same_str_sort(col_key_inst, col_values, value):
    col_key_tmp = []
    for match in col_key_inst:
        val = col_values[match[2]][match[1]]
        col_key_tmp.append((val.strip()
                            != value.strip(), match[0], match[2], val))  #

    col_key_tmp.sort()
    return col_key_tmp