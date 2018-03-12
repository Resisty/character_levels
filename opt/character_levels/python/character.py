#!/usr/bin/python
# =======================================
#
#  File Name : character.py
#
#  Purpose :
#
#  Creation Date : 10-01-2016
#
#  Last Modified : Mon 12 Mar 2018 04:44:09 PM CDT
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

HREF = 'http://us.battle.net/wow/en/character/%s/simple'
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
    character_detail = peewee.TextField(null = True)
    render = peewee.TextField(null = True)
    realm_name = peewee.TextField(unique = True)
    href = peewee.TextField(default = HREF)

    class Meta:
        database = psql_db

def create_characters():
    psql_db.connect()
    psql_db.create_tables([Character])
    for realm, chars in cfg['characters'].iteritems():
        for char in chars:
            realm_name = realm + '/' + char
            try:
                Character.create(realm_name=realm_name,
                                 href=HREF % realm_name)
            except peewee.IntegrityError:
                psql_db.connect()

def drop_characters():
    psql_db.connect()
    psql_db.drop_tables([Character])

def update_characters():
    psql_db.connect()
    for i in Character.select():
        s = scraper.Scraper(i.realm_name)
        character_detail = s.stats['details']
        level = s.stats['level']
        render = s.render
        modified = datetime.datetime.now()
        query = (Character.update(modified = modified,
                                  level = level,
                                  character_detail = character_detail,
                                  render = render,
                                  href = HREF % i.realm_name)
                          .where(Character.realm_name == i.realm_name))
        query.execute()

def get_characters():
    chars = Character.select().order_by(Character.realm_name)
    characters = []
    for i in chars:
        char = model_to_dict(i)
        name, realm = i.realm_name.split('/')
        char['realm'], char['name'] = name.capitalize(), realm.capitalize()
        characters.append(char)
    return characters

def main():
    r = update_characters()

if __name__ == '__main__':
    main()
