#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
from flask import Flask, flash, redirect, render_template, request, url_for
from flask import session, Response, abort, jsonify, make_response, current_app
from flask import send_from_directory
from functools import wraps, update_wrapper
from datetime import timedelta
import urllib2, socket, struct, json, os
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

@app.route('/character_scrape', methods=['POST'])
def scrape_char():
    error = None
    stats_data = {'level': '0',
                  'race': 'N/A',
                  'spec tip': 'N/A',
                  'class': 'N/A'}
    if request.method == 'POST':
        try:
            char, realm = request.get_json()['character'], request.get_json()['realm']
            url = "http://us.battle.net/wow/en/character/{0}/{1}/simple"
            url = url.format(realm, char)
            html = urllib2.urlopen(url).read()
            stats = {'level': 'span',
                     'race': 'a',
                     'spec tip': 'a',
                     'class': 'a'}
            stats_data = {attr: soup_find_text(html, tag, attr) for attr, tag in stats.iteritems()}
        except:
            pass # continue on and return default (meaningless) json if
                 # something goes wrong
        stats_data['character'] = char
        stats_data['realm'] = realm
    return jsonify(results=stats_data)

@app.route('/')
def indexpage():
    html_dir = os.path.join(static_root, 'html')
    return send_from_directory(html_dir, 'index.html')

@app.route('/js/<path:filename>')
def static_proxy(filename):
    # send_static_file will guess the correct MIME type
    js_dir = os.path.join(static_root, 'js')
    return send_from_directory(js_dir, filename)

def soup_find_text(html, tag, attr):
    soup = BeautifulSoup(html)
    return soup.body.find(tag, attrs={'class': attr}).text

if __name__ == '__main__':
    app.run(host='brianauron.info', port=8080, debug = True)
