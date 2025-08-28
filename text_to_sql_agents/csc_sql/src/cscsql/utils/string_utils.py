from typing import List

__all__ = [
    "StringUtils"
]


class StringUtils:

    @staticmethod
    def find_txt_in_string(string: str, search_string: str, ignore_case=False) -> bool:
        if ignore_case:
            string = string.lower()
        return string.find(search_string) != -1

    @staticmethod
    def clean_chess_str(name: str) -> str:
        if name is None:
            return name
        name = name.replace('\"', '').replace('`', '')
        return name
