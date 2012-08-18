from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('busitizer.core.views',
    url(r'^$', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^grab_photos/$', 'grab_photos'),
)