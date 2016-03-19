#!/usr/bin/python
# =======================================
#
#  File Name : scraper.py
#
#  Purpose :
#
#  Creation Date : 19-02-2015
#
#  Last Modified : Sat 19 Mar 2016 03:59:48 PM CDT
#
#  Created By : Brian Auron
#
# ========================================

from bs4 import BeautifulSoup
import requests, socket, struct, json, os
import traceback
from pprint import pprint

def soup_find_text(html, tag, attr):
    soup = BeautifulSoup(html)
    result = soup.body.find_all(tag, attrs={'class': attr})
    if len(result) == 1 and attr != 'profession-details':
        return result[0].text
    elif len(result) > 1 and attr == 'profession-details':
        return [i.find('span', 'name').text for i in result]
    elif result == []:
        return result
    else:
        return result[0].find('span', 'value').text

class Scraper(object):
    def __init__(self, realm_name):
        self._url = "http://us.battle.net/wow/en/character/%s/" % realm_name
        self._simple = self.url + "simple"
        self._html = None
        self._stats = None
        self._professions = {}

    @property
    def url(self):
        return self._url

    @property
    def simple(self):
        return self._simple

    @property
    def html(self):
        if not self._html:
            self._html = requests.get(self.url).text
        return self._html

    @property
    def stats(self):
        if not self._stats:
            stat_dict = {'level': 'span',
                         'race': 'a',
                         'spec tip': 'a',
                         'class': 'a'}
            self._stats  = ({attr: soup_find_text(self.html, tag, attr)
                              for attr, tag in stat_dict.iteritems()})
        return self._stats

    @property
    def professions(self):
        if not self._professions:
            profs =  [i.lower() for i in soup_find_text(self.html, 'a', 'profession-details')]
            profs += ['first-aid', 'archaeology', 'cooking', 'fishing']
            url = self.url + 'profession/%s'
            for i in profs:
                prof_url = url % i
                html = requests.get(prof_url).text
                prof_level = soup_find_text(html, 'a', 'profession-details')
                if prof_level == []:
                    continue
                prof_nums = [float(j.strip()) for j in prof_level.split('/')]
                self._professions[i] = {}
                self._professions[i]['string'] = prof_level
                ratio = int(prof_nums[0] / prof_nums[1] * 100)
                self._professions[i]['ratio'] = ratio if ratio <= 100 else 100
        return self._professions

    def getStats(self):
        return self.stats

    def getProfs(self):
        return self.professions

def main():
    realm_name = 'gilneas/resisty'
    s = Scraper(realm_name)
    print 'Gilneas/Resisty stats:'
    print s.stats
    print 'Gilneas/Resisty professions:'
    print s.professions

if __name__ == '__main__':
    main()
