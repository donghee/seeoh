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
    tong2 = SeeOhClient(_feed='74539')
    tong2_tweepy.api.update_status(u'통이 입니다. 온도는 %(temp)s도, 습도가 %(humidity)s퍼센트, 땅의 수분은 %(moisture)s퍼센트, 밝기는 %(light)s 입니다.  - %(now)s'% 
        {"temp":tong2.get_temperature(), 
         "humidity":tong2.get_humidity(), 
         "moisture":tong2.get_moisture(), 
         "light":tong2.get_light(),
         "now":now})
    dokgi = SeeOhClient(_feed='74540')
    dokgi_tweepy.api.update_status(u'난 독기야~. 온도: %(temp)s도, 습도: %(humidity)s퍼센트. 땅의 수분: %(moisture)s퍼센트. 밝기: %(light)s. - %(now)s'% 
        {"temp":dokgi.get_temperature(), 
         "humidity":dokgi.get_humidity(), 
         "moisture":dokgi.get_moisture(), 
         "light":dokgi.get_light(), 
         "now":now})
  return True

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

if __name__ == '__main__':
  app.run(host = '0.0.0.0', debug = True)
