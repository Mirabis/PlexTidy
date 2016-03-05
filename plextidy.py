import configparser
import datetime
import logging
import os
import shutil
import time

####
## Read config files etc
####
from logging.handlers import RotatingFileHandler
from operator import itemgetter

import sys

cfg = configparser.ConfigParser()
try:
    cfg.read('/config/plextidy.cfg')
except:  # Normal
    cfg.read('plextidy.cfg')

####
## Setup Basic Logging functionality
####
logging.basicConfig(level=str(cfg.get(section='PATHS', option='log_level',fallback='DEBUG')), format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('plextidy')
logger.addHandler(RotatingFileHandler(
    filename=os.path.join(str(cfg.get(section='PATHS', option='log_dir',fallback=".")),'plextidy.log'), mode='a', maxBytes=5000000,
    backupCount=3, encoding=None))


####
## Re-usable functions
####
def get_total_disk_space(path: str):
    return shutil.disk_usage(path)[0]


def get_used_disk_space(path: str):
    return shutil.disk_usage(path)[1]


def get_free_disk_space(path: str):
    return shutil.disk_usage(path)[2]


def get_disk_threshold(path: str):
    return get_used_disk_space(path) / get_total_disk_space(path)

def subdirs(path):
    """Yield directory names not starting with '.' under given path."""
    for entry in os.scandir(path):
        if not entry.name.startswith('.') and entry.is_dir():
            yield entry

def transcode_files(path:str,ext:str):
    """Yield file names with specified file extension"""
    for entry in os.scandir(path):
        try:
            if os.path.splitext(entry.name)[1] is ext:
                yield entry
        except Exception as e:
            logger.error("Unable to inspect file at:{0} -- {1}".format(path, str(e)))

def del_file(path: str):
    try:
        os.remove(path)
        logger.debug("Removed file at {0}".format(path))
    except Exception as e:
        logger.error("Unable to remove file at:{0} -- {1}".format(path, str(e)))


####
## Main code
####
def eval_threshold(path:str,thresh:int) -> int:
    return get_disk_threshold(path) > thresh / 1000


if __name__ == "__main__":
    try:
        threshold_exceeded = False
        deployMode=os.getenv('TRAVIS',False)
        cfg_interval = int(cfg.get(section='TIDY', option='interval', fallback=120))
        cfg_transcode_path = str(cfg.get(section='PATHS', option='transcode_path', fallback=os.path.curdir))
        cfg_threshold = int(cfg.get(section='TIDY', option='threshold', fallback=700))
        cfg_ext = str(cfg.get(section='TIDY', option='extension', fallback='.ts'))
        while True:
            threshold_exceeded = eval_threshold(path=cfg_transcode_path,thresh=cfg_threshold)
            if threshold_exceeded:
                logger.info("Disk Threshold has been exceeded, starting cleanup...")
                for dir in subdirs(cfg_transcode_path):
                    current_path = dir.path
                    timestamps = []
                    logger.info("Traversing {0} for garbage collection...".format(current_path))
                    for file in transcode_files(current_path,cfg_ext):
                        try:
                            assert isinstance(file.stat, os.stat_result)
                            timestamps.append((file.path, file.stat.st_mtime))
                        except Exception as e:
                            logger.warning("Failed to access: {0}".format(str(e)))
                    timestamps.sort(key=itemgetter(1))
                    for file, _ in timestamps[:len(timestamps) // 2]:
                        del_file(file)
                        logger.info("Finished tidying up {0}".format(current_path))
                if deployMode: # minimal impact?
                    exit(0)
            else:
                logger.debug("Entered waiting state, next run scheduled at: {0}",
                             (datetime.datetime.now() + datetime.timedelta(seconds=cfg_interval)).strftime("%H:%M:%S"))
                time.sleep(seconds=cfg_interval)
    finally:
        logger.info("PlexTidy terminated...")
