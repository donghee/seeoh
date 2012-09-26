# -*- coding: utf-8 -*-

from flask import Flask, url_for, render_template, session
from celery import Celery
from cosm import SeeOhClient
import celeryconfig
from tweepyconfig import *
import datetime

app = Flask(__name__)

app.config.setdefault('TONG2_CONSUMER_KEY', tong2_consumer_key)
app.config.setdefault('TONG2_CONSUMER_SECRET', tong2_consumer_secret)
app.config.setdefault('TONG2_ACCESS_TOKEN_KEY', tong2_access_token_key)
app.config.setdefault('TONG2_ACCESS_TOKEN_SECRET', tong2_access_token_secret)
 
app.config.setdefault('DOKGI_CONSUMER_KEY', dokgi_consumer_key )
app.config.setdefault('DOKGI_CONSUMER_SECRET', dokgi_consumer_secret)
app.config.setdefault('DOKGI_ACCESS_TOKEN_KEY', dokgi_access_token_key)
app.config.setdefault('DOKGI_ACCESS_TOKEN_SECRET', dokgi_access_token_secret)
 
dokgi_tweepy = Tweepy(app, config_prefix='DOKGI')
tong2_tweepy = Tweepy(app, config_prefix='TONG2')

celery = Celery(__name__)
celery.conf.add_defaults(app.config)
celery.config_from_object(celeryconfig)

@celery.task
def tweet():
  with app.test_request_context() as request:
    now = datetime.datetime.now().strftime("%Y-%m-%dT %H:%M")
    see = SeeOhClient(_feed='74539')
    humidity = see.get_humidity()
    status = tong2_tweepy.api.update_status(u'안녕하세요 통이 입니다. 습도가 %(humidity)s프로네. - %(now)s'% {"humidity":humidity, "now":now})
    status = dokgi_tweepy.api.update_status(u'안녕하세요 난 독기야~. 습도가 %(humidity)s프로네. 온도가 23도! - %(now)s'% {"humidity":humidity, "now":now})
  return True

@celery.task
def update_sensors():
  see = SeeOhClient(_feed='74539')
  print see.get_humidity()
  return

@app.route('/')
def index():
  see = SeeOhClient(_feed='74539')
  temperature = see.get_temperature()
  return render_template('index.html', temperature = temperature)

@app.route('/tweets')
def show_tweets():
  tweets = tong2_tweepy.api.user_timeline()
  tweets = tweets + dokgi_tweepy.api.user_timeline()
  print dir(tong2_tweepy.api)
  print dir(tweets[0])
  return render_template('tweets.html', tweets=tweets)

# @app.route('/post/<int:post_id>')
# def show_post(post_id):
  # return 'Post %d' % post_id

if __name__ == '__main__':
  app.run(host = '0.0.0.0', debug = True)
