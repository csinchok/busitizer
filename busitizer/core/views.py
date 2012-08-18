from celery import group

from busitizer.core.tasks import busitize

def async_busitize(request):
    # Get fb images, save them somewhere, then get this list.
    images = []
    busitize_group = group(busitize.s(  image, 
                                        user=request.user, 
                                        fb_id=fb_id,
                                        tags=tags,
                                        ignore=ignore) for image in images)
