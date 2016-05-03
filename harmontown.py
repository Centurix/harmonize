#!python2
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import requests
import os
import pprint
from time import gmtime, strftime, sleep

__description__ = 'Harmontown grabber.'
__author__ = 'Chris Read'
__version__ = '0.0.1'
__date__ = '2016/05/03'

EXIT_OK = 0
EXIT_OTHER_ERROR = 1
EXIT_PARAM_ERROR = 2

"""
http://download.harmontown.com/video/harmontown-2016-05-01-final.mp4
http://download.harmontown.com/video/harmontown-2016-04-24-final.mp4
http://download.harmontown.com/video/harmontown-2016-04-17-final.mp4
http://download.harmontown.com/video/harmontown-2016-04-10-final.mp4
http://download.harmontown.com/video/harmontown-2016-04-03-final.mp4
http://download.harmontown.com/video/harmontown-2016-03-27-final.mp4
http://download.harmontown.com/video/harmontown-2016-03-20-final.mp4
http://download.harmontown.com/video/harmontown-2016-03-13-final.mp4
"""

HARMONTOWN_URL = 'http://download.harmontown.com/video'
HARMONTOWN_DIRECTORY = 'temp'


def main():
    # file_name = 'harmontown-%s-final.mp4' % strftime('%Y-%m-%d')
    file_name = 'harmontown-2016-05-01-final.mp4'
    print('%s/%s' % (HARMONTOWN_URL, file_name))
    bytes = 0
    files = os.listdir(HARMONTOWN_DIRECTORY)
    with open(os.path.join(HARMONTOWN_DIRECTORY, file_name), 'wb') as handle:
        result = requests.get('%s/%s' % (HARMONTOWN_URL, file_name), stream=True)
        if not result.ok:
            print('No episode found')
            return EXIT_OK

        size = int(result.headers['content-length'])

        for block in result.iter_content(1024):
            print('Written %d Kb of %d Kb (%.2f%% complete)' % (bytes / 1024, size / 1024, float(bytes) / float(size) * 100), end="\r")
            # sys.stdout.write()
            # sys.stdout.flush()

            sleep(.01)
            bytes += 1024
            handle.write(block)

    return EXIT_OK

if __name__ == '__main__':
    sys.exit(main())
