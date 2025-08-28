import datetime
import time

from cscsql.utils.base_utils import BaseUtil


class TimeUtils(BaseUtil):
    STANDARD_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    STANDARD_DAY_FORMAT = "%Y-%m-%d"
    STANDARD_HOUR_FORMAT = "%H:%M:%S"
    STANDARD_TIME_SHORT_FORMAT = "%Y%m%d_%H%M%S"
    GPU_TIME_FORMAT = "%Y/%m/%d %H:%M:%S.%f"

    def init(self):
        pass

    @staticmethod
    def now():
        return datetime.datetime.now()

    @staticmethod
    def now_str(time_format="%Y-%m-%d %H:%M:%S"):
        return time.strftime(time_format, time.localtime())

    @staticmethod
    def now_str_short(time_format="%Y%m%d_%H%M%S"):
        return TimeUtils.now_str(time_format)

    @staticmethod
    def now_day_and_str_short():
        return f"{TimeUtils.get_time()}/{TimeUtils.now_str_short()}"

    @staticmethod
    def get_time():
        return time.strftime("%Y-%m-%d", time.localtime())
