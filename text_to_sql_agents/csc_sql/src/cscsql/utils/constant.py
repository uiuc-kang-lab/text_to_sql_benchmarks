import os


def get_user_home():
    return os.path.expanduser("~")


def get_value_from_env_or_default(default: str, env_key: str = None):
    if env_key is None:
        return default
    return default if not os.getenv(env_key) else os.getenv(env_key)


def getenv(env_key: str, default="") -> str:
    return get_value_from_env_or_default(default=default, env_key=env_key)


USER_HOME = get_user_home()


class Constants(object):

    USER_HOME = get_user_home()
    SRC_WORK_DIR = f"{USER_HOME}/work/csc_sql"

    SRC_HOME_DIR = getenv("SRC_HOME_DIR", default=SRC_WORK_DIR)
    SRC_DATA_HOME_DIR = f"{SRC_HOME_DIR}/data"

    OUTPUT_DIR = getenv("OUTPUT_DIR", f"{SRC_HOME_DIR}/outputs")
    LOG_HOME = f"{OUTPUT_DIR}/logs"

    NLP_DATA_DIR = f"{USER_HOME}/work"

    LOG_FILE = f"{LOG_HOME}/run.log"
    LOG_LEVEL = "info"

    DELIMITER_TAB = "\t"

    DATASET_DIR = getenv("DATASET_DIR", f"{USER_HOME}/work")
    DATASET_NAME = getenv("DATASET_NAME", "bird")
    DATASET_MODE = getenv("DATASET_MODE", "dev")

    TRAIN_FILE_NAME = getenv("TRAIN_FILE_NAME", f"{DATASET_DIR}/{DATASET_NAME}/train/train.json")
    DEV_FILE_NAME = getenv("DEV_FILE_NAME", f"{DATASET_DIR}/{DATASET_NAME}/dev/dev.json")
    TEST_FILE_NAME = getenv("TEST_FILE_NAME", f"{DATASET_DIR}/{DATASET_NAME}/test/test.json")

    EVAL_FILE_NAME = TEST_FILE_NAME if DATASET_MODE == 'test' else DEV_FILE_NAME

    SQL_DATASET_DIR = getenv("SQL_DATASET_DIR", DATASET_DIR)
    SQL_DATASET_DIR_TRAIN = getenv("SQL_DATASET_DIR_TRAIN", f"{DATASET_DIR}/{DATASET_NAME}/train/train_databases")
    SQL_DATASET_DIR_DEV = getenv("SQL_DATASET_DIR_DEV", f"{DATASET_DIR}/{DATASET_NAME}/dev/dev_databases")

