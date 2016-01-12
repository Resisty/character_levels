#!/usr/bin/python
# =======================================
#
#  File Name : scraper.py
#
#  Purpose :
#
#  Creation Date : 19-02-2015
#
#  Last Modified : Tue 12 Jan 2016 01:49:03 AM CST
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
        self.url = "http://us.battle.net/wow/en/character/{}/"
        self.url = self.url.format(realm_name)
        self.simple = self.url + "simple"
        html = self.__getCharacterHTML__()
        self.stats = self.__getCharacterStats__(html)
        self.professions = self.__getCharacterProfs__(html)

    def __getCharacterHTML__(self):
        return requests.get(self.url).text

    def __getCharacterStats__(self, html):
        stats = {'level': 'span',
                 'race': 'a',
                 'spec tip': 'a',
                 'class': 'a'}
        return {attr: soup_find_text(html, tag, attr) for attr, tag in stats.iteritems()}

    def __getCharacterProfs__(self, html):
        profs =  [i.lower() for i in soup_find_text(html, 'a', 'profession-details')]
        profs += ['first-aid', 'archaeology', 'cooking', 'fishing']
        url = self.url + 'profession/{}'
        profession_details = {}
        for i in profs:
            prof_url = url.format(i)
            html = requests.get(prof_url).text
            prof_level = soup_find_text(html, 'a', 'profession-details')
            if prof_level == []:
                continue
            prof_nums = [float(j.strip()) for j in prof_level.split('/')]
            profession_details[i] = {}
            profession_details[i]['string'] = prof_level
            ratio = int(prof_nums[0] / prof_nums[1] * 100)
            profession_details[i]['ratio'] = ratio if ratio <= 100 else 100
        return profession_details

    def getStats(self):
        return self.stats

    def getProfs(self):
        return self.professions

def main():
    realm_name = 'gilneas/resisty'
    s = Scraper(realm_name)
    print 'Gilneas/Resisty stats:'
    print s.getStats()
    print 'Gilneas/Resisty professions:'
    print s.getProfs()

if __name__ == '__main__':
    main()
