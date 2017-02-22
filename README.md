**Harmonize** - Harmontown downloading script.

Set this up with a cron job or some other scheduling tool, copy example.cfg to harmonize.cfg. Edit and change your
settings for the destination folder. This script will automatically scan for and download video episodes of Harmontown.

Currently this script is setup to make Plex compatible filenames:

`Harmontown - S01E117 - 2014-09-21.mp4`

The date is included here to make this script much simpler, otherwise we're fiddling with Wordpress feeds and
thetvdb.com queries, which prior versions of this script did...

Season and episode naming follows thetvdb.com naming. Everything appears in season 1. Should really be by year but
whatever.

There's a setting to turn the downloading of HQ videos on and off.

Uses Python 2.x, but could probably survive a quick upgrade using the newer configparser library

I've only tested this under Linux, should work in Windows, YMMV

Included copies of older scripts which do funky things with feeds and thetvdb.com queries.
