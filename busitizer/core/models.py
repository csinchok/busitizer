import datetime

from django.db import models
from django.contrib.auth.models import User

class Photo(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    original = models.ImageField(upload_to='originals')
    busitized = models.ImageField(upload_to='busitized')
    fb_id = models.IntegerField(null=True, blank=True)
    tweet_id = models.BigIntegerField(null=True, blank=True)
    source = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(default=datetime.datetime.now())
