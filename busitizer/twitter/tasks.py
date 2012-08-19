from django.conf import settings

import celery
import requests
import twitpic
import urlparse
from bs4 import BeautifulSoup

from busitizer.core.tasks import busitize

twitpic = twitpic.TwitPicOAuthClient(
    consumer_key = settings.TWITPIC_CONSUMER_KEY,
    consumer_secret = settings.TWITPIC_CONSUMER_TOKEN,
    access_token = settings.TWITPIC_ACCESS_TOKEN,
    service_key = settings.TWITPIC_SERVICE_KEY
)

def random_status(params={'username': '@chrissinchok'}):
    statuses = [
        "%(username)s YOU DONE GOT BUSEY'D, SON.",
        "Hey %(username)s, I perked your picture up a little bit. Hope you like it.",
        "%(username)s I saw your pic, and thought \"You know what this needs? Some Gary Busey\". You're welcome.",
        "%(username)s Not enough Busey. Don't worry, I fixed it for you.",
        "%(username)s MORE BUSEY.",
        "%(username)s Gary Busey really classes up pictures very nicely."
        "%(username)s As Gary himself once said: \"Bird season is over, butthorn.\". You're welcome.",
        "%(username)s Your pic was badly in need of a little Busey. But then again, what isn't?",
        "%(username)s As Gary once said: \"Drinking your own blood is the paradigm of recycling.\". He was right on the money.",
        "%(username)s As Gary says: \"Great things like this only happen for the first time once\".",
        "%(username)s As Gary himself once said: \"He's like a one legged cat trying to bury a turd on a frozen pond.\"",
        "%(username)s As the man himself once said: \"Fear is the dark room where the Devil develops his negatives\". Think about it.",
        "%(username)s Let me Busey that up for you a little.",
        "%(username)s Busey is as Busey does.",
        "%(username)s WE ARE ALL BUSEY, EVERY ONE OF US.",
        "%(username)s Sometimes you just gotta add some Busey.",
        "%(username)s Were you in Point Break? No, of course not. But Gary Busey was.",
        "%(username)s I can't wait for Piranha 3DD, can you?",
        "%(username)s Too little Busey. I have rectified this for you.",
        "%(username)s I upped the Busey levels in this picture. I think it's better now.",
        "%(username)s MORE BUSEY.",
        "%(username)s I went ahead and Busey'd this up a little bit",
    ]
    return random.choice(statuses) % params

@celery.task
def handle_tweet(tweet):
    url = tweet['entities']['urls']['expanded_url']
    response = requests.get(url)
    cookies = response.cookies
    if response.headers.get('content_type').contains('image/'):
        image_name = os.path.basename(urlparse.urlparse(response.url).path)
        image_path = os.path.join(settings.TEST_IMAGES, image_name)
        image_file = open(image_path, 'w')
        image_file.writer(response.content)
        busitize.delay(image_path, tweet_id=tweet['id'])
        return
    
    soup = BeautifulSoup(response.text)
    images = []
    for tag in soup.find_all('img'):
        image = {'url': tag.get('src')}
        
        images.append({
            'url': tag.get('src'),
            'width': int(tag.get('width', '0')),
            'height': int(tag.get('height', '0')),
        })
    sorted_images = sorted(images, key=lambda image: image['width'] + image['height'])
    print(tweet)