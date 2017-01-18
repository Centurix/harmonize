#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os
import re
import datetime
import requests

__description__ = 'Harmonize.'
__author__ = 'Chris Read'
__version__ = '0.0.1'
__date__ = '2017/01/18'

EXIT_OK = 0
EXIT_OTHER_ERROR = 1
EXIT_PARAM_ERROR = 2

HARMONTOWN_URL = 'http://download.harmontown.com/video'
HARMONTOWN_DIRECTORY = '/plex/TV/Comedy/Harmontown/Season 01'
#HARMONTOWN_DIRECTORY = '/home/chris/Desktop'

# http://download.harmontown.com/video/harmontown-2017-01-15-final.mp4


def last_episode():
    highest_episode = 116  # The first regular video episode available online, 2014-11-01
    year = 2014
    month = 9
    day = 1

    # Get the last episode downloaded, must be a relationship between the date and the episode number somehow
    for filename in os.listdir(HARMONTOWN_DIRECTORY):
        matches = re.match('Harmontown - S01E(\d+) - (\d+)-(\d+)-(\d+)\.mp4', filename)
        if matches and int(matches.group(1)) > highest_episode:
            highest_episode = int(matches.group(1))
            year = int(matches.group(2))
            month = int(matches.group(3))
            day = int(matches.group(4))

    return highest_episode, datetime.date(year, month, day)


def main():
    last = last_episode()
    # Find the latest download from the site
    end_date = datetime.datetime.now().date()
    last_date = last[1]
    last_date += datetime.timedelta(days=1)
    while last_date <= end_date:
        file_name = 'harmontown-%s-final.mp4' % last_date
        request = requests.get('%s/%s' % (HARMONTOWN_URL, file_name), stream=True)
        if request.ok:
            print('Found %s' % file_name)
            out_file_name = 'Harmontown - S01E%d - %s.mp4' % (last[0] + 1, last_date)
            print('Output file: %s' % out_file_name)
            size = int(request.headers['content-length'])
            bytes_received = 0
            if not os.path.isfile(os.path.join(HARMONTOWN_DIRECTORY, out_file_name)):
                with open(os.path.join(HARMONTOWN_DIRECTORY, out_file_name), 'wb') as handle:
                    for block in request.iter_content(1024):
                        print('Written %d Kb of %d Kb (%.2f%% complete)' % (
                            bytes_received / 1024,
                            size / 1024,
                            float(bytes_received) / float(size) * 100
                        ), end="\r")
                        bytes_received += 1024
                        handle.write(block)

        last_date += datetime.timedelta(days=1)

    return EXIT_OK

if __name__ == '__main__':
    sys.exit(main())
