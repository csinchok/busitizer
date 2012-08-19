from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from busitizer.core.views import PhotoDetailView

urlpatterns = patterns('busitizer.core.views',
    url(r'^$', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^grab_photos\.json$', 'grab_photos'),
    url(r'^poll_completion/(?P<task_id>[a-z0-9-]{36})\.json$', 'poll_completion'),
    url(r'^photo/(?P<pk>\d+)$', PhotoDetailView.as_view(), name='photo-detail'),
    url(r'^photo/(?P<pk>\d+)/delete$', 'delete_photo')
    
)