import random
import uuid
import json

from celery import group

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse

from busitizer.core.tasks import get_photos
                                    
def grab_photos(request):
    
    facebook_auth = request.user.social_auth.filter(provider='facebook')
    if facebook_auth.count() == 1:
        token = facebook_auth[0].tokens['access_token']
        result = get_photos.delay(request.user, token=token)
        cache.set(result.task_id, False)
        data = {'success': True, 'message': 'Working...', 'task_id': result.task_id}
    else:
        data = {'success': False, 'message': 'Not logged in!'}
    
    return HttpResponse(json.dumps(data), mimetype="application/json")
    

    # print(photos)
    # 
    # fb = get_persistent_graph(request)
    # 
    # photos = fb.get('me/photos')
    # 
    # data = photos['data']
    # random.shuffle(data)
    # photos = data[:settings.BUSEY_COUNT]
    # 
    # _uuid = uuid.uuid1()
    # 
    # cache.set(str(_uuid), settings.BUSEY_COUNT)
    
    # for photo in photos:
        # result = download_image.apply_async((photo,), link=busitize.s(request.user, fb_id=photo['id'], tags=photo['tags']['data']))
    
    # return HttpResponse(json.dumps(photos), mimetype="application/json")
    
