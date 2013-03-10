from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('busitizer.core.views',
    url(r'^$', TemplateView.as_view(template_name="home.html"), name="home"),
    url(r'^busitize', 'busitize'),
)

urlpatterns += staticfiles_urlpatterns()