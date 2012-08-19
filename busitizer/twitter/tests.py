import os

from django.test import TestCase
from django.conf import settings
from busitizer.twitter.tasks import handle_tweet

class TestTwitterBotTask(TestCase):
        
    def test_image_url_tweet(self):
        
        test_data = '{"text":"@BUSITIZER Celery is the best. http:\/\/t.co\/p5Nibzsd","entities":{"hashtags":[],"urls":[{"indices":[31,51],"url":"http:\/\/t.co\/p5Nibzsd","display_url":"twitpic.com\/show\/large\/akl\u2026","expanded_url":"http:\/\/twitpic.com\/show\/large\/akv0vv"}],"user_mentions":[{"indices":[0,10],"id_str":"471652063","name":"The Buseytizer","screen_name":"BUSITIZER","id":471652063}]},"id":237293014131810304,"in_reply_to_screen_name":"BUSITIZER","in_reply_to_user_id":471652063}'
        handle_tweet.delay(test_data)
            

    def test_image_page_tweet(self):
        test_data = '{"text":"@BUSITIZER Celery is the best. http:\/\/t.co\/p5Nibzsd","entities":{"hashtags":[],"urls":[{"indices":[31,51],"url":"http:\/\/t.co\/p5Nibzsd","display_url":"twitpic.com\/show\/large\/akl\u2026","expanded_url":"http:\/\/imgur.com\/gallery\/1xOjy"}],"user_mentions":[{"indices":[0,10],"id_str":"471652063","name":"The Buseytizer","screen_name":"BUSITIZER","id":471652063}]},"id":237293014131810304,"in_reply_to_screen_name":"BUSITIZER","in_reply_to_user_id":471652063}'
        handle_tweet.delay(test_data)