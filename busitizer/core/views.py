import random
import uuid
import json

from celery import group
from celery.result import AsyncResult

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.template.loader import render_to_string

from busitizer.core.tasks import get_photos
from busitizer.core.models import Photo
      
def poll_completion(request, task_id):
    data = {'completed': False}
    result = AsyncResult(task_id)
    if result.ready():
        data['completed'] = True
        photo = result.result
        data['html'] = render_to_string('snippets/photo.html', {'photo': photo})
        data['url'] = photo.get_absolute_url()
    return HttpResponse(json.dumps(data), mimetype="application/json")
                              
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
    
class PhotoDetailView(DetailView):

    model = Photo
    context_object_name = 'photo'
    template_name = 'photo_detail.html'