import glob
import json
import os

import traceback

import jsonlines

from cscsql.utils.base_utils import BaseUtil
from cscsql.utils.logger_utils import logger


class FileUtils(BaseUtil):

    def init(self):
        pass

    @staticmethod
    def save_to_text(filename, content, mode='w'):
        """
        保存为文本
        :param filename:
        :param content:
        :return:
        """
        try:
            FileUtils.check_file_exists(filename)
            with open(filename, mode, encoding='utf-8') as f:
                f.writelines(content)
        except Exception as e:
            traceback.print_exc()
            logger.warning(f"保存文件失败：{filename} - {content[:10]}")

    @staticmethod
    def save_to_file(filename, content, mode='wb'):
        """
        保存为文本
        :param filename:
        :param content:
        :param mode:
        :return:
        """
        try:
            FileUtils.check_file_exists(filename)
            with open(filename, mode) as f:
                f.write(content)
                f.flush()
        except Exception as e:
            traceback.print_exc()
            logger.warning(f"保存文件失败：{filename}")

    @staticmethod
    def get_content(path, encoding='gbk'):
        """
        读取文本内容
        :param path:
        :param encoding:
        :return:
        """
        with open(path, 'r', encoding=encoding, errors='ignore') as f:
            content = ''
            for l in f:
                l = l.strip()
                content += l
            return content

    @staticmethod
    def get_file_name_list(path, type="*.txt"):
        """获取指定路径下的指定类型的所有文件"""
        files = glob.glob(os.path.join(path, type))
        return files

    @staticmethod
    def get_file_line(file_name):
        """
        获取文件 行数
        :param file_name:
        :return:
        """
        count = 0
        with open(file_name, encoding="utf-8") as f:
            for line in f:
                count += 1
        return count

    @staticmethod
    def get_file_name(file_name, add_end=False):
        """
        获取文件名称
        :param file_name:
        :param add_end:
        :return:
        """
        if file_name is None or len(file_name) < 1:
            return ""

        file_dir, name = os.path.split(file_name)
        raw_name, end = os.path.splitext(name)
        return name if add_end else raw_name

    @staticmethod
    def get_file_name_without_end(file_name):
        """
        获取文件名称
        :param file_name:
        :return:
        """
        if file_name is None or len(file_name) < 1:
            return ""

        file_dir, name = os.path.split(file_name)
        raw_name, end = os.path.splitext(name)
        raw_file_name = os.path.join(file_dir, raw_name)
        return raw_file_name

    @staticmethod
    def get_raw_file_name(file_name):
        """
        获取文件名称
        :param file_name:
        :return:
        """
        return FileUtils.get_file_name(file_name=file_name, add_end=True)

    @staticmethod
    def check_file_exists(filename, delete=False):
        """检查文件是否存在"""
        if filename is None:
            return False
        dir_name = os.path.dirname(filename)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            print("文件夹不存在,创建目录:{}".format(dir_name))
        return os.path.exists(filename)

    @staticmethod
    def get_file_parent_dir_name(file_name):
        file_dir, name = os.path.split(file_name)
        parent_dir = FileUtils.get_file_name(f"{file_dir}.txt")
        return parent_dir

    @staticmethod
    def list_dir_or_file(file_dir, add_parent=False, sort=False, start_with=None, is_dir=True,
                         end_with=None, reverse=False):
        """
        读取文件夹下的所有子文件夹
        :param file_dir:
        :param add_parent:
        :param sort:
        :param start_with:
        :param is_dir:
        :param end_with:
        :return:
        """
        dir_list = []
        if not os.path.exists(file_dir):
            return dir_list
        for name in os.listdir(file_dir):
            run_dir = os.path.join(file_dir, name)
            flag = os.path.isdir(run_dir) if is_dir else os.path.isfile(run_dir)
            if flag:
                if start_with is not None and not str(name).startswith(start_with):
                    continue
                if end_with is not None and not str(name).endswith(end_with):
                    continue
                if add_parent:
                    run_dir = os.path.join(file_dir, name)
                else:
                    run_dir = name
                dir_list.append(run_dir)

        if sort:
            dir_list.sort(key=lambda k: str(k), reverse=reverse)

        return dir_list

    @staticmethod
    def list_dir(file_dir, add_parent=False, sort=False, start_with=None, end_with=None, reverse=False):
        """
        读取文件夹下的所有子文件夹
        :param file_dir:
        :param add_parent:
        :param sort:
        :param start_with:
        :param end_with:
        :return:
        """
        return FileUtils.list_dir_or_file(file_dir=file_dir, add_parent=add_parent, sort=sort,
                                          start_with=start_with, end_with=end_with, is_dir=True, reverse=reverse)

    @staticmethod
    def list_file_prefix(file_dir, add_parent=False, sort=False, start_with=None, end_with=None, reverse=False):
        """
        读取文件夹下的所有文件
        :param file_dir:
        :param add_parent:
        :param sort:
        :param start_with: 文件前缀
        :param end_with:
        :return:
        """
        return FileUtils.list_dir_or_file(file_dir=file_dir, add_parent=add_parent, sort=sort,
                                          start_with=start_with, end_with=end_with, is_dir=False, reverse=reverse)

    @staticmethod
    def save_to_json(filename, content):
        """
        保存map 数据
        :param filename:
        :param maps:
        :return:
        """
        FileUtils.check_file_exists(filename)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False)

    @staticmethod
    def load_json(filename) -> json:
        if not os.path.exists(filename):
            return dict()

        with open(filename, 'r', encoding='utf8') as f:
            return json.load(f)

    @staticmethod
    def load_jsonl(filename):
        if not os.path.exists(filename):
            return []

        result = jsonlines.open(filename)
        return result

    @staticmethod
    def dump_json(fp, obj, sort_keys=False, indent=4, show_info=False):
        try:
            fp = os.path.abspath(fp)
            if not os.path.exists(os.path.dirname(fp)):
                os.makedirs(os.path.dirname(fp), exist_ok=True)
            with open(fp, 'w', encoding='utf8') as f:
                json.dump(obj, f, ensure_ascii=False, sort_keys=sort_keys, indent=indent, separators=(',', ':'))
            if show_info:
                logger.info(f'json 文件保存成功，{fp}')
            return True
        except Exception as e:
            traceback.print_exc()
            logger.info(f'json 文件 {fp} 保存失败, {e}')
            return False

    @staticmethod
    def dump_json_string(obj, sort_keys=False, ):
        """
        序列化 json string
        :param obj:
        :param sort_keys:
        :return:
        """
        json_str = json.dumps(obj, ensure_ascii=False, sort_keys=sort_keys, separators=(',', ':'))
        return json_str

    @staticmethod
    def read_to_text(path, encoding='utf-8'):
        """读取txt 文件"""
        with open(path, 'r', encoding=encoding) as f:
            content = f.read()
            return content

    @staticmethod
    def read_to_text_list(path, encoding='utf-8'):
        """
        读取txt文件,默认utf8格式,
        :param path:
        :param encoding:
        :return:
        """
        list_line = []
        if not os.path.exists(path):
            return list_line
        with open(path, 'r', encoding=encoding) as f:
            list_line = f.readlines()
            list_line = [row.rstrip("\n") for row in list_line]
            return list_line
