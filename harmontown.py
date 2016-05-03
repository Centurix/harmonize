#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import requests
import os
import pprint
import datetime
import feedparser
from time import mktime
from lxml import etree
import string

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
HARMONTOWN_FEED = 'http://www.harmontown.com'

TVDB_API_KEY = '475D69C4508A56E1'
TVDB_SERIES_ID = '301912'
TVDB_URL = 'http://thetvdb.com/api'

"""
http://thetvdb.com/api/475D69C4508A56E1/mirrors.xml
http://thetvdb.com/api/GetEpisodeByAirDate.php?apikey=475D69C4508A56E1&seriesid=301912&airdate=2015-01-25
<mirrorpath>/api/GetEpisodeByAirDate.php?apikey=475D69C4508A56E1&seriesid=301912&airdate=2015-01-25
"""

delta = datetime.timedelta(days=1)
max_delta = datetime.timedelta(days=6)


def format_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    return filename


def main():
    start_date = HARMONTOWN_START
    try:
        with open('last_date', 'r') as handle:
            start_date = datetime.datetime.strptime(handle.readline(), '%Y-%m-%d').date()
    except IOError as ie:
        print('No last episode found, starting from the beginning')
    end_date = datetime.datetime.now().date()
    start_date += delta
    while start_date <= end_date:
        """
        This needs to be Harmontown - S01E195 - What did you do to Norman Lear?.mp4
        """
        file_name = 'harmontown-%s-final.mp4' % start_date
        request = requests.get('%s/%s' % (HARMONTOWN_URL, file_name), stream=True)
        if request.ok:
            print('Found an episode: %s, downloading...' % file_name)
            episode_name = '%s' % start_date
            episode_number = '%s' % start_date

            tvdb_info = requests.get(
                '%s/GetEpisodeByAirDate.php' % TVDB_URL,
                params={
                    'apikey': TVDB_API_KEY,
                    'seriesid': TVDB_SERIES_ID,
                    'airdate': start_date
                }
            )
            if tvdb_info.ok:
                root = etree.fromstring(tvdb_info.content)
                if len(root.xpath('.//EpisodeName')) > 0:
                    episode_name = root.xpath('.//EpisodeName')[0].text
                if len(root.xpath('.//EpisodeNumber')) > 0:
                    episode_number = root.xpath('.//EpisodeNumber')[0].text

            out_file_name = 'Harmontown - S01E%s - %s.mp4' % (episode_number, episode_name)
            size = int(request.headers['content-length'])
            bytes_received = 0
            with open(os.path.join(HARMONTOWN_DIRECTORY, out_file_name), 'wb') as handle:
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
