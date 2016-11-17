#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import datetime
import requests
import os

__description__ = 'Harmongrab.'
__author__ = 'Chris Read'
__version__ = '0.0.1'
__date__ = '2016/11/17'

EXIT_OK = 0
EXIT_OTHER_ERROR = 1
EXIT_PARAM_ERROR = 2

"""
.downloaded.txt

http://download.harmontown.com/video/harmontown-2014-09-21-final.mp4

"""

HARMONTOWN_URL = 'http://download.harmontown.com/video'
HARMONTOWN_DIRECTORY = '/home/chris/Desktop'
# HARMONTOWN_DIRECTORY = '/media/TV/Comedy/Harmontown/Season 01'
HARMONTOWN_DOWNLOADED = '.downloaded.txt'
HARMONTOWN_START = datetime.date(2014, 9, 21)
HARMONTOWN_EPISODE_NUMBER = 117


def main():
    downloaded_episodes = list()
    current_episode_number = HARMONTOWN_EPISODE_NUMBER

    if not os.path.isfile(HARMONTOWN_DOWNLOADED):
        open(HARMONTOWN_DOWNLOADED, 'w')

    with open(HARMONTOWN_DOWNLOADED, 'r+') as handle:
        downloaded_episodes = handle.readlines()

    with open(HARMONTOWN_DOWNLOADED, 'a') as handle:
        start_date = HARMONTOWN_START
        end_date = datetime.datetime.now().date()

        while start_date <= end_date:
            filename = 'harmontown-%s-final.mp4' % start_date
            start_date += datetime.timedelta(days=1)

            if 'downloaded,%s\r\n' % filename in downloaded_episodes:
                current_episode_number += 1
                continue

            if 'missing,%s\r\n' % filename in downloaded_episodes:
                continue

            request = requests.get('%s/%s' % (HARMONTOWN_URL, filename), stream=True)

            if request.ok:
                print('Found an episode: %s (%d)' % (filename, current_episode_number))
                out_file_name = 'Harmontown - S01E%d.mp4' % current_episode_number
                current_episode_number += 1
                size = int(request.headers['content-length'])
                bytes_received = 0
                if not os.path.isfile(os.path.join(HARMONTOWN_DIRECTORY, out_file_name)):
                    print('No existing file found, downloading')
                    with open(os.path.join(HARMONTOWN_DIRECTORY, out_file_name), 'wb') as handle2:
                        for block in request.iter_content(1024):
                            print('Written %d Kb of %d Kb (%.2f%% complete)' % (
                                bytes_received / 1024,
                                size / 1024,
                                float(bytes_received) / float(size) * 100
                            ), end="\r")
                            bytes_received += 1024
                            handle2.write(block)
                handle.write('downloaded,%s\r\n' % filename)
            elif start_date < end_date:
                handle.write('missing,%s\r\n' % filename)

    return EXIT_OK


if __name__ == '__main__':
    sys.exit(main())
