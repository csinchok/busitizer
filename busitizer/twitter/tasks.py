from django.conf import settings

import celery
import requests
import twitpic
import urlparse
import json
import os
from bs4 import BeautifulSoup
import tweepy
import random

from busitizer.core.tasks import busitize_url

twitpic = twitpic.TwitPicOAuthClient(
    consumer_key = settings.TWITPIC_CONSUMER_KEY,
    consumer_secret = settings.TWITPIC_CONSUMER_TOKEN,
    access_token = settings.TWITPIC_ACCESS_TOKEN,
    service_key = settings.TWITPIC_SERVICE_KEY
)

def random_status(params={'username': '@chrissinchok'}):
    statuses = [
        ".@%(username)s YOU DONE GOT BUSEY'D, SON.",
        ".@%(username)s, I perked your picture up a little bit. Hope you like it.",
        ".@%(username)s I saw your pic, and thought \"You know what this needs? Some Gary Busey\". You're welcome.",
        "@%(username)s Not enough Busey. Don't worry, I fixed it for you.",
        ".@%(username)s MORE BUSEY.",
        "@%(username)s Gary Busey really classes up pictures very nicely."
        ".@%(username)s As Gary himself once said: \"Bird season is over, butthorn.\". You're welcome.",
        "@%(username)s Your pic was badly in need of a little Busey. But then again, what isn't?",
        ".@%(username)s As Gary once said: \"Drinking your own blood is the paradigm of recycling.\".",
        ".@%(username)s As Gary says: \"Great things like this only happen for the first time once\".",
        ".@%(username)s As Gary himself said: \"He's like a one legged cat trying to bury a turd on a frozen pond.\"",
        "@%(username)s As the man himself said: \"Fear is the dark room where the Devil develops his negatives\". Think about it.",
        "@%(username)s Let me Busey that up for you a little.",
        ".@%(username)s Busey is as Busey does.",
        ".@%(username)s WE ARE ALL BUSEY, EVERY ONE OF US.",
        "@%(username)s Sometimes you just gotta add some Busey.",
        "@%(username)s Were you in Point Break? No, of course not. But Gary Busey was.",
        ".@%(username)s I can't wait for Piranha 3DD, can you?",
        ".@%(username)s Too little Busey. I have rectified this for you.",
        "@%(username)s I upped the Busey levels in this picture. I think it's better now.",
        "@%(username)s MORE BUSEY.",
        ".@%(username)s I went ahead and Busey'd this up a little bit",
    ]
    return random.choice(statuses) % params

@celery.task
def send_tweet(photo, original_tweet):
    if photo is None:
        return
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(settings.TWITTER_OAUTH_KEY, settings.TWITTER_OAUTH_SECRET)
    api = tweepy.API(auth)
    
    status_text = random_status(params={'username': original_tweet['user']['screen_name']})
    print('tweeting %s' % status_text)
    twitpic_response = twitpic.create('upload', params={'message': status_text, 'media': photo.busitized.path})
    api.update_status("%s %s" % (status_text, twitpic_response['url']))
    return None

@celery.task
def handle_tweet(tweet):
    tweet = json.loads(tweet)
    url = tweet['entities']['urls'][0]['expanded_url']
    response = requests.get(url)
    cookies = response.cookies
    if 'image/' in response.headers.get('content-type', ''):
        busitize_url.apply_async([response.url,], {'tweet_id': tweet['id']}, link=send_tweet.s(tweet))
        return None
    
    parse_url = urlparse.urlparse(response.url)
    domain_string = "%s://%s" % (parse_url.scheme, parse_url.netloc)
    
    soup = BeautifulSoup(response.text)
    images = []
    for tag in soup.find_all('img'):
        image = {'url': tag.get('src')}
        url = tag.get('src')
        if url.startswith('/'):
            url = domain_string + url

        try:
            response = requests.head(url, allow_redirects=True)
        except:
            continue
        length = int(response.headers.get('content-length', '0'))
        filename, extension = os.path.splitext(urlparse.urlparse(response.url).path)
        if 'image/' in response.headers.get('content-type', ''):
            if extension in ['.jpg', '.jpeg', '.png']:
                try:
                    images.append({
                        'url': response.url,
                        'length': length
                    })
                except Exception as e:
                    continue
    sorted_images = sorted(images, key=lambda image: image['length'])
    busitize_url.apply_async([sorted_images[-1]['url'],], {'tweet_id': tweet['id']}, link=send_tweet.s(tweet))
    return None