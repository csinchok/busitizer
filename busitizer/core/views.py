import random
import uuid
import json
import os

from celery import group
from celery.result import AsyncResult

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth import logout

from busitizer.core.tasks import get_photos
from busitizer.core.models import Photo
      
def poll_completion(request, task_id):
    """
    This view is polled every second, checking to see if the task is done.
    Once it is, it rendes the HTML for the image display, and passes it along.
    """
    
    data = {'completed': False}
    result = AsyncResult(task_id)
    
    # Sometimes we get weird image and/or network errors returned
    if result.ready() and not isinstance(result.result, Exception):
        data['completed'] = True
        photo = result.result
        data['html'] = render_to_string('snippets/photo.html', {'photo': photo})
        data['url'] = photo.get_absolute_url()
    return HttpResponse(json.dumps(data), mimetype="application/json")
                              
def grab_photos(request):
    """
    A view to initiate the Busitization process. This puts the task in celery, 
    and gives the task id to javascript, which uses it to check the status of
    the task by calling 'poll_completion'.
    """
    
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
    """
    View to allow a user to delete a photo, because we're nice.
    """

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
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
    
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