-----------------------------------------
[![Build Status](https://travis-ci.org/Mirabis/PlexTidy.svg?branch=master)](https://travis-ci.org/Mirabis/PlexTidy)
[![GitHub issues](https://img.shields.io/github/issues/Mirabis/PlexTidy.svg)](https://github.com/Mirabis/PlexTidy/issues)
[![GitHub forks](https://img.shields.io/github/forks/Mirabis/PlexTidy.svg?style=flat-square)](https://github.com/Mirabis/PlexTidy/network)
-----------------------------------------
# PlexTidy
PlexTidy is a small python3 script to cleanup your transcode directory to allow processing on small (ram)disks.

## Using PlexTidy
* Use it directly through Python3, visit the [GitHub Release!](https://github.com/Mirabis/PlexTidy/releases) page to download the script.
* Use it through PlexPy, as described in: `TODO`
* Use my docker-image available at https://github.com/Mirabis/docker-plextidy 

### Configurable Options

The variables are honored to configure your instance:

* `GROUP_ID`	=	Unix Group ID (Default 1994)
* `USER_ID`	=	Unix user id (Default 1994)
* `LOG_LEVEL`	=	Logging Directory (Default DEBUG (can be INFO, WARNING, ERROR, DEBUG)
* `DISK_THRESHOLD`	=	Disk full threshold (Default 700 (e.g. 70%))
* `DISK_INTERVAL`	=	How often we should check the directory (Default 60s)
* `FILE_EXTENSION`	=	File extension filter for plex transcode files (Default '.ts')

The plextidy.cnf file contains additional information on each variable.


### Issues

If you have any problems with or questions about this image, please contact me through a [GitHub issue!](/issues).