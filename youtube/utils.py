import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def clean_int(int_num):
    new_int = 0
    try:
        new_int = int(int_num)
    except Exception:
        logger.info("Parameter is not an integer, setting to zero")
    return new_int

def clean_float(float_num):
    new_float = 0.0
    try:
        new_float = float(float_num)
    except Exception:
        logger.info("Parameter is not a float, setting to zero")
    return new_float

def clean_last_time(last_time):
    new_last_time = datetime.now()
    try:
        datetime.strptime(last_time,'%Y-%m-%dT%H:%M:%S.000Z')
    except:
        logger.info("Last time is malformed, defaulting to now")
    return new_last_time
