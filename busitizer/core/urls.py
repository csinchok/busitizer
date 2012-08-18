from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('busitzer.core.views',
    url(r'^$', TemplateView.as_view(template_name="home.html"), name="home"),
)