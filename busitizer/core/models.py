import datetime
from urllib import urlencode

from django.db import models

class Image(models.Model):

    PENDING = 202
    FAILED = 404
    COMPLETED = 200
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (FAILED, 'Failed'),
        (COMPLETED, 'Completed')
    )

    url = models.URLField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    created = models.DateTimeField(default=datetime.datetime.now)
    busitized = models.ImageField(upload_to='busitized')

    def __unicode__(self):
        return self.url

    def get_absolute_url(self):
        return "/busitize?%s" % urlencode({'url': self.url})