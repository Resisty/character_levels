#!/usr/bin/python
# =======================================
#
#  File Name : character.py
#
#  Purpose :
#
#  Creation Date : 10-01-2016
#
#  Last Modified : Tue 12 Jan 2016 09:16:12 AM CST
#
#  Created By : Brian Auron
#
# ========================================

import datetime
import peewee
import os
import yaml
import json
import scraper
from playhouse.postgres_ext import PostgresqlExtDatabase
from playhouse.shortcuts import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
yaml_loc = os.path.join(BASE_DIR, 'character_scraper.yaml')
with open(yaml_loc, 'r') as fptr:
    cfg = yaml.load(fptr.read())
dbuser = cfg['dbuser']
dbpass = cfg['dbpass']
db = cfg['db']
psql_db = PostgresqlExtDatabase(db, user = dbuser, password = dbpass)

class Character(peewee.Model):
    modified = peewee.DateTimeField(default = datetime.datetime.now())
    level = peewee.TextField(null = True)
    race = peewee.TextField(null = True)
    spec_tip = peewee.TextField(null = True)
    charclass = peewee.TextField(null = True)
    professions = peewee.TextField(null = True)
    realm_name = peewee.TextField(unique = True)

    class Meta:
        database = psql_db

def create_characters():
    psql_db.connect()
    psql_db.create_tables([Character])
    for realm, chars in cfg['characters'].iteritems():
        for char in chars:
            Character.create(realm_name = realm + '/' + char)

def update_characters():
    psql_db.connect()
    for i in Character.select():
        s = scraper.Scraper(i.realm_name)
        stats = s.getStats()
        profs = s.getProfs()
        modified = datetime.datetime.now()
        level = stats['level']
        race = stats['race']
        spec_tip = stats['spec tip']
        charclass = stats['class']
        professions = json.dumps(profs)
        query = (Character.update(modified = modified,
                                  level = level,
                                  race = race,
                                  spec_tip = spec_tip,
                                  charclass = charclass,
                                  professions = professions)
                          .where(Character.realm_name == i.realm_name))
        query.execute()

def get_characters():
    chars = Character.select().order_by(Character.realm_name)
    characters = []
    for i in chars:
        char = model_to_dict(i)
        try:
            char['professions'] = json.loads(char['professions'])
        except TypeError:
            char['professions'] = None
        name, realm = i.realm_name.split('/')
        char['realm'], char['name'] = name.capitalize(), realm.capitalize()
        characters.append(char)
    return characters

def main():
    r = update_characters()

if __name__ == '__main__':
    main()
