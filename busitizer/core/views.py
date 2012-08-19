import random
import uuid
import json

from celery import group

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse

from busitizer.core.tasks import busitize

from django_facebook.api import get_persistent_graph, FacebookUserConverter, require_persistent_graph
from django_facebook.connect import CONNECT_ACTIONS, connect_user
from django_facebook.decorators import facebook_required   
                                    

@facebook_required(scope='user_photos')
def grab_photos(request):
    fb = get_persistent_graph(request)
    
    photos = fb.get('me/photos')
    
    data = photos['data']
    random.shuffle(data)
    photos = data[:settings.BUSEY_COUNT]
    
    _uuid = uuid.uuid1()
    
    cache.set(str(_uuid), settings.BUSEY_COUNT)
    
    # for photo in photos:
        # result = download_image.apply_async((photo,), link=busitize.s(request.user, fb_id=photo['id'], tags=photo['tags']['data']))
    
    return HttpResponse(str(_uuid))
    
