import logging
import os
import time
from logging import handlers

from cscsql.utils.constant import Constants


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, filename, level='info', when='D', backCount=3,
                 fmt='%(asctime)s %(levelname)s %(pathname)s[%(lineno)d]: %(message)s'):
        filename_str = filename
        self.filename = filename
        self.logger = logging.getLogger(filename_str)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        th = handlers.TimedRotatingFileHandler(filename=filename_str, when=when, backupCount=backCount,
                                               encoding='utf-8')
        th.setFormatter(format_str)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)


def get_day():
    return time.strftime("%Y-%m-%d", time.localtime())

def get_time():
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())


def get_log_file_name(file_name):
    src_dir_name = os.path.dirname(file_name)
    base_name = os.path.basename(file_name)
    index = str(base_name).rindex(".")
    pre_name = str(base_name)[:index]
    last_name = str(base_name)[index:]
    log_file = f"{src_dir_name}/{get_day()}/{pre_name}_{get_time()}{last_name}"
    print(log_file)
    dir_name = os.path.dirname(log_file)
    os.makedirs(dir_name, exist_ok=True)
    return log_file


logger = Logger(filename=get_log_file_name(Constants.LOG_FILE), level=Constants.LOG_LEVEL).logger
