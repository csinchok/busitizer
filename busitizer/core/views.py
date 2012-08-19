import random
import uuid
import json
import os

from celery import group
from celery.result import AsyncResult

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response

from busitizer.core.tasks import get_photos
from busitizer.core.models import Photo
      
def poll_completion(request, task_id):
    data = {'completed': False}
    result = AsyncResult(task_id)
    if result.ready() and not isinstance(result.result, Exception):
        data['completed'] = True
        photo = result.result
        data['html'] = render_to_string('snippets/photo.html', {'photo': photo})
        data['url'] = photo.get_absolute_url()
    return HttpResponse(json.dumps(data), mimetype="application/json")
                              
def grab_photos(request):
    
    busey_level = request.GET.get('busey_level', 4)
    
    facebook_auth = request.user.social_auth.filter(provider='facebook')
    if facebook_auth.count() == 1:
        token = facebook_auth[0].tokens['access_token']
        result = get_photos.delay(request.user, token=token, busey_count=busey_level)
        cache.set(result.task_id, False)
        data = {'success': True, 'message': 'Working...', 'task_id': result.task_id}
    else:
        data = {'success': False, 'message': 'Not logged in!'}
    
    return HttpResponse(json.dumps(data), mimetype="application/json")
    
def delete_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if photo.user != request.user:
        message = "You don't have permissions to delete this photo."
    else:
        try:
            os.remove(photo.busitized.path)
        except:
            pass
        try:
            os.remove(photo.original.path)
        except:
            pass
        photo.delete()
        message = "Photo deleted."
        
    return render_to_response("delete_photo.html", context_instance=RequestContext(request, {'message': message}))
    
class PhotoDetailView(DetailView):

    model = Photo
    context_object_name = 'photo'
    template_name = 'photo_detail.html'
    
class PhotoListView(ListView):
    def get_queryset(self):
        return Photo.objects.all()

    context_object_name = 'photo_list'
    template_name = 'photo_gallery.html'
    paginate_by = 10
    
    
class MyPhotoListView(PhotoListView):
    def get_queryset(self):
        return Photo.objects.filter(user__id=self.request.user.id)
        
    template_name = 'my_gallery.html'