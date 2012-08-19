import os

from django.test import TestCase
from django.conf import settings
from busitizer.twitter.tasks import handle_tweet

class TestTwitterBotTask(TestCase):
        
    def test_image_url(self):
        
        test_images = [os.path.join(settings.TEST_IMAGES, filename) for filename in os.listdir(settings.TEST_IMAGES)]
        for image_path in test_images:
            response = busitize.delay(image_path)