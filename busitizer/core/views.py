import random
import uuid
import json
import os

from celery import group
from celery.result import AsyncResult

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import logout

from busitizer.core.tasks import get_photos
from busitizer.core.models import Image


def busitize(request):
    if 'url' not in request.GET:
        raise HttpResponseBadRequest

    url = request.GET['url']
    image, created = Image.objects.get_or_create(url=url)

    if created:
        response_code = 201
    else:
        response_code = image.status

    # TODO: test accept header

    return render(request, "busitize.html", {'image': image}, status=response_code)
