from flask import Flask, render_template, request, Response, jsonify
import requests
import tweepy
import os
import json
import random
import arrow
import time

app = Flask(__name__)

APP_KEY = os.environ.get('APP_KEY')
API_KEY = os.environ.get('TROVE_API_KEY')
TITLES = os.environ.get('TITLES')
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')


def tweet(message):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.update_status(message)


def truncate(message, length):
  if len(message) > length:
    message = '{}...'.format(message[:length])
  return message


def prepare_message(item):
    message = 'Another interesting article! {}: {}'
    details = None
    if item['zone'] == 'article':
        date = arrow.get(item['date'], 'YYYY-MM-DD')
        details = '{}, \'{}\''.format(date.format('D MMM YYYY'), truncate(item['heading'].encode('utf-8'), 200))
    if details:
        message = message.format(details, item['troveUrl'].replace('ndp/del', 'newspaper'))
    else:
        message = None
    return message


def save_max(zones):
    max = get_current_max(zones)
    if not os.path.exists('.data'):
        os.makedirs('.data')
    with open(os.path.join('.data', 'max.json'), 'wb') as max_file:
        json.dump({'max': max}, max_file)


def get_last_max():
    try:
        with open(os.path.join('.data', 'max.json'), 'rb') as max_file:
            last = json.load(max_file)
            max = last['max']
    except IOError:
        max = 0
    return max


def get_current_max(zones):
    max = 0
    for zone in zones:
        total = int(zone['records']['total'])
        if total > max:
            max = total
    return max


def authorised(request):
    if request.args.get('key') == APP_KEY:
        return True
    else:
        return False


@app.route('/')
def home():
    return 'hello, I\'m ready to tweet'


def prepare_titles():
    titles = ['l-title={}'.format(title) for title in TITLES.split(',')]
    return '&'.join(titles)


@app.route('/random/')
def tweet_random():
    status = 'nothing to tweet'
    if authorised(request):
        max = get_last_max()
        titles = prepare_titles()
        print max
        start = random.randrange(0, max + 1)
        url = 'http://api.trove.nla.gov.au/result/?q=+&zone=newspaper&l-category=Article&{}&encoding=json&n=1&s={}&key={}'.format(titles, start, API_KEY)
        print url
        response = requests.get(url)
        if response.ok:
            data = response.json()
            items = []
            zones = data['response']['zone']
            save_max(zones)
            for zone in zones:
                if 'article' in zone['records']:
                    for item in zone['records']['article']:
                        item['zone'] = 'article'
                        items.append(item)
            if items:
                item = random.choice(items)
                message = prepare_message(item)
                if message:
                    print message
                    tweet(message)
                    status = 'ok, I tweeted something random'
        else:
            status = 'sorry, couldn\'t get data from Trove'
    else:
        status = 'sorry, not authorised to tweet'
    return status
