import re

class ColumnUpdater:
    def __init__(self, db_col):
        self.db_col = db_col
        self.col_table = self.build_col_table(db_col)  # 在初始化时构建列表

    def build_col_table(self, db_col):
        """构建列到表的映射"""
        col_table = {}
        for x in db_col:  # db_col: table.`column`
            table, col = x.split('.')
            col_table.setdefault(col, []).append(table)
        return col_table

    def col_pre_update(self, col, col_retrieve, foreign_set):
        """更新列集合"""
        cols = set(col.split(", ")).union(col_retrieve).union(foreign_set)

        cols = set([x.strip() for x in cols])
        cols = self.col_update(cols)
        return cols

    def col_update(self, cols_tmp):
        """更新列的格式为 table.`column`,加入同名列"""
        cols = []  # 所有 column 格式统一
        for c in cols_tmp:
            try:
                table, col_name = c.split('.')
                col_name = col_name.replace('`', '')
                col_name = self.quote_field(col_name)
                for t in self.col_table.get(col_name, []):
                    cols.append(f"{t}.{col_name}")  # 都变成 table.`xxx`
            except ValueError:
                # 捕获 ValueError，以防止 c 无法拆分
                pass
        return set(cols)

    def quote_field(self,field_name):
        # 正则表达式判断字段名是否包含空格或特殊字符
        if re.search(r'\W', field_name):
            # 如果匹配到，给字段名添加反引号
            return f"`{field_name}`"
        else:
            # 否则，不做改变
            return field_name
        
    def col_suffix(self,cols):
        col_info = self.col_check(cols)
        col_info = sorted(list(col_info))
        cols_sub = '\n'.join(col_info)
        return cols_sub
    
    def col_check(self,cols):
        ans = []
        for col in cols:
            ans.append(f"{col}: {self.db_col[col]}")
        return set(ans)




