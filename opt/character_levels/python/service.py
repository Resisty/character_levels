#!/usr/bin/env python
import character
import os
from flask import Flask, flash, redirect, render_template, request, url_for
from flask import session, Response, abort, jsonify, make_response, current_app
from functools import wraps, update_wrapper
from datetime import timedelta
from pprint import pprint


static_root = os.path.abspath('/opt/character_levels')
# Create a thread to execute function func
# with arguments args. Args must be a list
def spinoff_thread(func,args,kwargs=None):
    thr = threading.Thread(target=func,args=args,kwargs=kwargs)
    thr.daemon = True
    thr.start()

app = Flask(__name__, static_url_path=os.path.abspath(os.path.curdir))
app.secret_key = os.urandom(32)

@app.errorhandler(404)
def page_not_found(e):
    try:
        img_dir = os.path.join(static_root, 'img')
    except Exception as e:
        return ('Well met!'), 404
    return send_from_directory(img_dir, 'wellmet.png'), 404

@app.errorhandler(500)
def page_not_found_500(e):
    try:
        img_dir = os.path.join(static_root, 'img')
    except Exception as e:
        return ('Well met!'), 500
    return send_from_directory(img_dir, 'wellmet.png'), 500

@app.route('/', methods=['GET'])
def scrape_char():
    error = None
    if request.method == 'GET':
        character.psql_db.connect()
        characters = character.get_characters()
        total = sum([int(i['level']) for i in characters])
        # Warlords of Draenor: max level 110
        maximum = 110 * len(characters)
        character_info = {'total': total,
                          'maximum': maximum,
                          'characters': characters}
        return jsonify(character_info = character_info)

if __name__ == '__main__':
    app.run(host='brianauron.info', port=8080, debug = True)
