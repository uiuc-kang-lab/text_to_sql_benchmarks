import json
import re


class MatchUtils(object):
    ENGLISH_PATTERN = re.compile(r"[a-zA-Z]")
    PATTERN_ENGLISH_AND_NUMBER = re.compile(r"[a-zA-Z0-9]")

    PATTERN_NONE_ZH = re.compile(r"[^\u4e00-\u9fa5]")
    PATTERN_ZH = re.compile(r"[\u4e00-\u9fa5]+")

    PATTERN_SQL_CREATE = re.compile(r"CREATE\s.*?;")

    PATTERN_NL2SQL_PREDICT_SQL = re.compile(r"```sql(.*)```")
    PATTERN_NL2SQL_PREDICT_SQL2 = re.compile(r"```(.*)```")

    PATTERN_SQL_SELECTION_1 = re.compile(r'(correct|chosen) candidate .{1,5}([AB])')
    PATTERN_SQL_SELECTION_2 = re.compile(r'(correct|chosen) answer.{1,5}([AB])')
    PATTERN_SQL_SELECTION_3 = re.compile(r'Candidate ([AB]) .{1,10} (correct|chosen)')
    PATTERN_SQL_SELECTION_3_2 = re.compile(r'candidate ([AB]) .{1,10} (correct|chosen)')
    PATTERN_SQL_SELECTION_4 = re.compile(r'candidate.{1,5}([AB])')
    PATTERN_SQL_SELECTION_4_2 = re.compile(r'[:：]([AB])')

    @staticmethod
    def clean_space(text: str) -> str:
        text = re.sub(r"\s", "", text)
        return text

    @staticmethod
    def match_none_zh(text):
        """
        匹配中文汉子
        :param text:
        :return:
        """
        return MatchUtils.match_pattern_flag(text, MatchUtils.PATTERN_NONE_ZH)

    @staticmethod
    def match_pattern_extract(text, pattern, return_str=False, **kwargs):
        """
        匹配单个位置
        :param text:
        :param pattern:
        :param return_str:
        :return:
        """
        if isinstance(pattern, str):
            match_pattern = re.compile(pattern)
        else:
            match_pattern = pattern

        match_result = match_pattern.findall(text, **kwargs)
        if len(match_result) > 0:
            if return_str:
                res = str(match_result[0]).rstrip()
            else:
                res = match_result
        else:
            res = ""
        return res

    @staticmethod
    def match_pattern_flag(text, pattern):
        """
        匹配结果
        :param text:
        :param pattern:
        :return:
        """
        flag = False
        filter_error_type = len(MatchUtils.match_pattern_extract(text, pattern)) > 0
        if filter_error_type:
            flag = True
        return flag

    @staticmethod
    def match_pattern_result(text, pattern):
        """
        匹配
        :param text:
        :param pattern:
        :return:
        """
        match_result = MatchUtils.match_pattern_extract(text, pattern)

        flag = False
        filter_error_type = len(match_result) > 0
        if filter_error_type:
            flag = True
        return flag, match_result

    @staticmethod
    def match_pattern_list(texts, pattern_list):
        """
        匹配  正则列表
        """
        if not isinstance(pattern_list, list):
            pattern_list = [pattern_list]

        match_result = []
        for pattern in pattern_list:
            raw_match_result = pattern.findall(texts)
            if len(raw_match_result) > 0:
                match_result = raw_match_result
                break

        return match_result

    @staticmethod
    def match_pattern_list_flag(texts, pattern_list):
        """
        匹配  正则列表
        :param texts:
        :param pattern_list:
        :return:
        """
        match_result = MatchUtils.match_pattern_list(texts=texts, pattern_list=pattern_list)

        return len(match_result) > 0

    @staticmethod
    def get_create_sql(text: str):
        result = re.findall(MatchUtils.PATTERN_SQL_CREATE, text, re.DOTALL)
        return result

    @staticmethod
    def extract_sql_selection_predict(text: str, return_str=False) -> str:
        """
        预测的 nl2sql 提取 sql
        Args:
            text:
            return_str:

        Returns:

        """
        pattern_list = [
            MatchUtils.PATTERN_SQL_SELECTION_1,
            MatchUtils.PATTERN_SQL_SELECTION_2,
            MatchUtils.PATTERN_SQL_SELECTION_3,
            MatchUtils.PATTERN_SQL_SELECTION_3_2,
            MatchUtils.PATTERN_SQL_SELECTION_4,
            MatchUtils.PATTERN_SQL_SELECTION_4_2,
        ]

        match_result = MatchUtils.match_pattern_list(texts=text.replace("\n", " "), pattern_list=pattern_list)

        if len(match_result) > 0:
            if return_str:
                res = str(match_result[0]).rstrip()
            else:
                res = match_result
        else:
            res = ""
        return res

    @staticmethod
    def extract_sql_selection_result(predict: str):
        result = "A"

        if predict.find("{") > -1 and predict.find("}") > -1:
            try:
                parse_predict = predict[:predict.find("}") + 1]
                raw = json.loads(parse_predict.replace("\n", " "))
                result = raw["choose"]

                if len(result) > 1:
                    match_result = MatchUtils.extract_sql_selection_predict(result)
                    if match_result:
                        result = match_result[0]

            except Exception as e:
                # traceback.print_exc()
                show = predict.replace("\n", " ")
                print(f'json parse error: {show}')
                pass

            result = result.upper()
            return result

        if len(predict) == 1:
            result = predict[0]
        elif len(predict) > 1:
            if predict.upper().startswith("A"):
                result = "A"
            elif predict.upper().startswith("B"):
                result = "B"
            else:
                match_result = MatchUtils.extract_sql_selection_predict(predict)
                if match_result:
                    result = match_result[0]
        try:
            if not isinstance(result, str) and len(result) > 1:
                result = result[0]
            result = result.upper()
        except Exception as e:
            print(f"extract_sql_selection_result error: {predict} - {result}")
            result = "A"
        return result
