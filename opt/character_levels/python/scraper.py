#!/usr/bin/python
# =======================================
#
#  File Name : scraper.py
#
#  Purpose :
#
#  Creation Date : 19-02-2015
#
#  Last Modified : Mon 12 Mar 2018 04:45:53 PM CDT
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
        self._html = None
        self._stats = None
        self._render = None

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
            stats = (BeautifulSoup(self.html, 'html5lib')
                     .findAll('div', 'CharacterHeader-detail'))
            details = ' '.join([i.string for i in stats])
            tokens = details.split(' ')
            level, details = tokens[0], ' '.join(tokens[1:])
            self._stats = {'level': level,
                           'details': details}
        return self._stats

    @property
    def render(self):
        if not self._render:
            render = (BeautifulSoup(self.html, 'html5lib')
                      .find('div',
                            'CharacterProfile-export')
                      .next
                      .attrs['href'])
            self._render = render
            if not self._render:
                self._render = 'No rendered image available.'
        return self._render

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
    realm_name = 'cenarius/resistidari'
    s = Scraper(realm_name)
    print 'Cenarius/bediviere stats:'
    print s.stats
    print 'Cenarius/bediviere professions:'
    print s.professions

if __name__ == '__main__':
    main()
