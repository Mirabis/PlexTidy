-----------------------------------------
[![Build Status](https://travis-ci.org/Mirabis/PlexTidy.svg?branch=master)](https://travis-ci.org/Mirabis/PlexTidy)
[![GitHub issues](https://img.shields.io/github/issues/Mirabis/PlexTidy.svg)](https://github.com/Mirabis/PlexTidy/issues)
[![GitHub forks](https://img.shields.io/github/forks/Mirabis/PlexTidy.svg?style=flat-square)](https://github.com/Mirabis/PlexTidy/network)
-----------------------------------------
# PlexTidy
PlexTidy is a small python3 script to cleanup your transcode directory to allow processing on small (ram)disks.

## Using PlexTidy
* Use it directly through Python3(.5+), visit the [GitHub Release!](https://github.com/Mirabis/PlexTidy/releases) page to download the script.
* Use my docker-image available at https://github.com/Mirabis/docker-plextidy (not working atm)

```bash
pip3 install scandir --upgrade
*/1 * * * * python3 plextidy.py [OPTIONS]

```
### Configurable Options

The variables are honored to configure your instance:

* `-t, --disk-threshold`	=	Disk full threshold (Default 700 (e.g. 70%))
* `-i,--disk-interval`	=	Period in seconds between disk threshold checks. The default interval is 60 seconds. Higher quality source media and a smaller disk size require more frequent threshold checks A higher disk threshold (speficied by the user) will also require more frequent checks;
* `-p,--disk-path`	=	Path to the temporary working directory used by the Plex New Transcoder. The transcode_path can be modified from the Plex web through Settings -> Server -> General -> Advanced;
* `-f,--file-regex`	=	The temporary file regex (default should be fine);
* `-l,--log-level`	=	Logging Level DEBUG, INFO, WARNING, ERROR (DEBUG is not advised);
* `-d,--log-dir`	=	Log directory (default script dir) for logrotating.
* `-o,--one-off`   = Run only once, in-case you run from cron (default=false)

### Automation
If you need help for additional configuration/automation/persistency please check my [Blog Post](https://mirabis.nl/development/docker-plextidy/)

### Credits
I'd like to thank https://gitlab.com/wjb/Plex-Free-Mem for the initial idea (No UNIX support).

### Issues

If you have any problems with or questions about this image, please contact me through a [GitHub issue!](/issues).
