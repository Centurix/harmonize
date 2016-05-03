#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import requests
import os
import datetime

__description__ = 'Harmontown grabber.'
__author__ = 'Chris Read'
__version__ = '0.0.1'
__date__ = '2016/05/03'

EXIT_OK = 0
EXIT_OTHER_ERROR = 1
EXIT_PARAM_ERROR = 2

"""
http://download.harmontown.com/video/harmontown-2015-01-25-final.mp4
"""

HARMONTOWN_URL = 'http://download.harmontown.com/video'
HARMONTOWN_DIRECTORY = 'temp'
HARMONTOWN_START = datetime.date(2015, 1, 25)

delta = datetime.timedelta(days=1)


def main():
    start_date = HARMONTOWN_START
    try:
        with open('last_date', 'r') as handle:
            start_date = datetime.datetime.strptime(handle.readline(), '%Y-%m-%d').date()
    except IOError as ie:
        print('No last episode found, starting from the beginning')
    end_date = datetime.datetime.now().date()
    while start_date <= end_date:
        file_name = 'harmontown-%s-final.mp4' % start_date
        request = requests.get('%s/%s' % (HARMONTOWN_URL, file_name), stream=True)
        if request.ok:
            print(start_date)
            size = int(request.headers['content-length'])
            bytes_received = 0
            with open(os.path.join(HARMONTOWN_DIRECTORY, file_name), 'wb') as handle:
                for block in request.iter_content(1024):
                    print('Written %d Kb of %d Kb (%.2f%% complete)' % (
                        bytes_received / 1024,
                        size / 1024,
                        float(bytes_received) / float(size) * 100
                    ), end="\r")
                    bytes_received += 1024
                    handle.write(block)

            with open('last_date', 'w') as handle:
                handle.write(start_date.strftime('%Y-%m-%d'))
        start_date += delta

    return EXIT_OK

if __name__ == '__main__':
    sys.exit(main())
