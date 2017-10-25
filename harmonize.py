#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os
import re
import datetime
import requests
import ConfigParser

"""
Harmonize - Harmontown downloading script.

Set this up with a cron job or some other scheduling tool, copy example.cfg to harmonize.cfg. Edit and change your
settings for the destination folder. This script will automatically scan for and download video episodes of Harmontown.

Currently this script is setup to make Plex compatible filenames:

Harmontown - S01E117 - 2014-09-21.mp4

* Note: Episode 117 was their test stream. There are a few audio episodes between that and their first official stream
in episode 126. This script will actually start with ep. 126. Downloading ep. 117 by itself is fairly straight forward.

The date is included here to make this script much simpler, otherwise we're fiddling with Wordpress feeds and
thetvdb.com queries, which prior versions of this script did...

Season and episode naming follows thetvdb.com naming. Everything appears in season 1. Should really be by year but
whatever.

This script just concentrates on downloading the 'standard' definition files, not the HQ ones that sometimes appear.

Uses Python 2.x, but could probably survive a quick upgrade using the newer configparser library

I've only tested this under Linux, should work in Windows, YMMV

Also, don't peel carrots. Subscribe to the podcast. $5 a month and you get to see:
* Rob Schrab shout CHIOPS
* Dan's baby dance
* Spencer smiling
* Jeff B. Davis not writing Teen Wolf.

"""

__description__ = 'Harmonize.'
__author__ = 'Chris Read'
__version__ = '0.0.1'
__date__ = '2017/01/18'

EXIT_OK = 0
EXIT_OTHER_ERROR = 1
EXIT_PARAM_ERROR = 2

ONE_DAY = datetime.timedelta(days=1)

config = ConfigParser.SafeConfigParser({'url': 'http://download.harmontown.com/video', 'destination': 'temp'})
config.read('harmonize.cfg')

HARMONTOWN_URL = config.get('DEFAULT', 'url')
HARMONTOWN_DIRECTORY = config.get('DEFAULT', 'destination')

BLOCK_READ_SIZE = 1024


def last_episode():
    """
    Scan for existing Harmontown episodes, find the latest one by file name, not file date and return it
    :return: Tuple of the last episode details
    """
    highest_episode = 125  # The one before the first regular video episode available online
    highest_date = datetime.date(2014, 11, 3)

    for filename in os.listdir(HARMONTOWN_DIRECTORY):
        matches = re.match('Harmontown - S01E(\d+) - (\d+)-(\d+)-(\d+)\.mp4', filename)
        if matches and int(matches.group(1)) > highest_episode:
            highest_episode = int(matches.group(1))
            highest_date = datetime.date(
                int(matches.group(2)),
                int(matches.group(3)),
                int(matches.group(4))
            )

    return highest_episode, highest_date


def main():
    last_episode_number, last_date = last_episode()

    last_episode_number += 1
    last_date += ONE_DAY
    end_date = datetime.datetime.now().date()

    while last_date <= end_date:
        file_name = 'harmontown-%s-final.mp4' % last_date
        file_name_hq = 'harmontown-%s-h265.mp4' % last_date
        request = requests.get('%s/%s' % (HARMONTOWN_URL, file_name), stream=True)

        if request.ok:
            if config.get('DEFAULT', 'hq') == 'true':
                hq_test = requests.get('%s/%s' % (HARMONTOWN_URL, file_name_hq), stream=True)
                if hq_test.ok:
                    request = hq_test
                    file_name = file_name_hq

            dest_file_name = 'Harmontown - S01E%d - %s.mp4' % (last_episode_number, last_date)
            size = int(request.headers['content-length'])
            bytes_received = 0
            print('Found %s, saving video to: %s' % (file_name, dest_file_name))
            with open(os.path.join(HARMONTOWN_DIRECTORY, dest_file_name), 'wb') as handle:
                for block in request.iter_content(BLOCK_READ_SIZE):
                    if block:
                        print('Written %d Kb of %d Kb (%.2f%% complete)' % (
                            bytes_received / 1024,
                            size / 1024,
                            float(bytes_received) / float(size) * 100
                        ), end="\r")
                        bytes_received += BLOCK_READ_SIZE
                        handle.write(block)
            last_episode_number += 1

        last_date += ONE_DAY

    return EXIT_OK

if __name__ == '__main__':
    sys.exit(main())
