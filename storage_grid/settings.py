import os.path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config')
UTILS_PATH=os.path.join(ROOT_DIR,'utils')
LOG_PATH = os.path.join(ROOT_DIR, 'logs')
ETC_PATH = os.path.join(ROOT_DIR, 'etc')
LOG_CFG_PATH = os.path.join(CONFIG_PATH, 'log')
SCHEMA_PATH = os.path.join(ETC_PATH, 'schema')
MODELS_PATH = os.path.join(ROOT_DIR,'models')

