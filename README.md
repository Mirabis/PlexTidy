-----------------------------------------
[![Build Status](https://travis-ci.org/Mirabis/PlexTidy.svg?branch=master)](https://travis-ci.org/Mirabis/PlexTidy)
[![GitHub issues](https://img.shields.io/github/issues/Mirabis/PlexTidy.svg)](https://github.com/Mirabis/PlexTidy/issues)
[![GitHub forks](https://img.shields.io/github/forks/Mirabis/PlexTidy.svg?style=flat-square)](https://github.com/Mirabis/PlexTidy/network)
-----------------------------------------
# PlexTidy
PlexTidy is a small python3 script to cleanup your transcode directory to allow processing on small (ram)disks.

## Using PlexTidy
* Use it directly through Python3, visit the [GitHub Release!](https://github.com/Mirabis/PlexTidy/releases) page to download the script.
* Use my docker-image available at https://github.com/Mirabis/docker-plextidy 

```shell
$ python plextidy.py --log-level 'DEBUG' --disk-threshold 700 --disk-interval 60 --file-extension '.ts'


### Configurable Options

The variables are honored to configure your instance:

* `GROUP_ID`	=	Unix Group ID (Default 1994)
* `USER_ID`	=	Unix user id (Default 1994)
* `LOG_LEVEL`	=	Logging Directory (Default DEBUG (can be INFO, WARNING, ERROR, DEBUG)
* `DISK_THRESHOLD`	=	Disk full threshold (Default 700 (e.g. 70%))
* `DISK_INTERVAL`	=	How often we should check the directory (Default 60s)
* `FILE_EXTENSION`	=	File extension filter for plex transcode files (Default '.ts')

The plextidy.cnf file contains additional information on each variable.

### Credits
I'd like to thank https://gitlab.com/wjb/Plex-Free-Mem for the initial idea (No UNIX support).

### Issues

If you have any problems with or questions about this image, please contact me through a [GitHub issue!](/issues).