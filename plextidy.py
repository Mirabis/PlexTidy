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
import argparse

####
## Accept Arguments
####
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--disk-threshold', default=700, type=int,
                    help="Disk full threshold (Default 700 (e.g. 70%))")
parser.add_argument('-i', '--disk-interval', default=60, type=int, help="Period in seconds between disk threshold checks. The default \
interval is 60 seconds. Higher quality source media and a smaller disk size require more frequent threshold checks \
A higher disk threshold (speficied by the user) will also require more frequent checks")
parser.add_argument('-p', '--disk-path', default='.', type=str, help="Path to the temporary working directory used by the \
Plex New Transcoder. The transcode_path can be modified from the Plex web through Settings -> Server -> General -> Advanced.")
parser.add_argument('-f', '--file-extension', default='.ts', type=str,
                    help="The file extension used for transcoded segments")
parser.add_argument('-l', '--log-level', default='WARNING', type=str,
                    help="Logging Level DEBUG, INFO, WARNING, ERROR (DEBUG is not advised)")
parser.add_argument('-d', '--log-dir', default='.', type=str, help="Log directory (default script dir) for logrotating")
parser.add_argument('-o', '--one-off', default=False, type=bool, help="Run only once, in-case you run from cron (default=false)")
args = parser.parse_args()

####
## Setup Basic Logging functionality
####
logging.basicConfig(level=args.log_level, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('plextidy')
logger.addHandler(
    RotatingFileHandler(filename=os.path.join(args.log_dir, 'plextidy.log'), mode='a', maxBytes=5000000,
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


def transcode_files(path: str, ext: str):
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

def tidy_disk(sleep:bool):
    threshold_exceeded = eval_threshold(path=cfg_transcode_path, thresh=cfg_threshold)
    if threshold_exceeded:
        logger.info("Disk Threshold has been exceeded, starting cleanup...")
        for dir in subdirs(cfg_transcode_path):
            current_path = dir.path
            timestamps = []
            logger.info("Traversing {0} for garbage collection...".format(current_path))
            for file in transcode_files(current_path, cfg_ext):
                try:
                    assert isinstance(file.stat, os.stat_result)
                    timestamps.append((file.path, file.stat.st_mtime))
                except Exception as e:
                    logger.warning("Failed to access: {0}".format(str(e)))
            timestamps.sort(key=itemgetter(1))
            for file, _ in timestamps[:len(timestamps) // 2]:
                del_file(file)
                logger.info("Finished tidying up {0}".format(current_path))
    else:
        logger.debug("Entered waiting state, next run scheduled at: {0}".format((datetime.datetime.now() + datetime.timedelta(seconds=cfg_interval)).strftime("%H:%M:%S")))
        if sleep:
            time.sleep(cfg_interval)
####
## Main code
####
def eval_threshold(path: str, thresh: int) -> int:
    return get_disk_threshold(path) > thresh / 1000


if __name__ == "__main__":
    try:
        threshold_exceeded=False
        cfg_interval = args.disk_interval
        cfg_transcode_path =  args.disk_path
        cfg_threshold =  args.disk_threshold
        cfg_ext = args.file_extension
        if args.one_off:
            tidy_disk(False)
            exit(0)
        else:
            while True:
                tidy_disk(True)
    except Exception as e:
        logger.error("Error has occurred, INFO:{0}".format(str(e)))
        exit(1)
    finally:
        logger.info("PlexTidy terminated...")

