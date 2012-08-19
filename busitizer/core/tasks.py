import os
import celery
import random
import requests
import urlparse
import facebook
import json

from django.conf import settings
from django.core.cache import cache

from busitizer.core.models import Photo
from busitizer.core.utils import Feature, eyes_valid, busitize_image

try:
    from cv2 import cv
    FACE_HC = cv.Load(os.path.join(settings.HAAR_CASCADES, "haarcascade_frontalface_default.xml"))
    EYE_HC = cv.Load(os.path.join(settings.HAAR_CASCADES, "haarcascade_eye.xml"))
except ImportError:
    print("You don't have OpenCV, so you won't be able to busitize :-(")
from PIL import Image

@celery.task
def get_photos(user, token=None):
    if token is None:
        token = user.social_auth.get(provider='facebook').tokens['access_token']
    graph = facebook.GraphAPI(token)
    photos_stream = graph.get_object("me/photos")
    photos = photos_stream['data']
    random.shuffle(photos)
    for photo in photos:
        result = busitize_url.delay(photo['source'], user=user, fb_id=photo['id'], fb_tags=photo['tags']['data'])
        try:
            photo = result.get(timeout=10)
        except Exception as e:
            print(e)
            break
        if photo:
            cache.set(get_photos.request.id, True)
            break
        

@celery.task
def busitize_url(image_url, user=None, fb_id=None, tweet_id=None, fb_tags=None, fb_ignore_tag=None, busey_count=5):
    """
    This task determines if an image is 'bustizable', and if so, busitizes it,
    returning the path of the busitized image. The algorithm is pretty strict,
    since we'd like to avoid incorrectly busitizing anything.
    
    Here's how the params work:
      image_path - Required, the absolute path to the image you would like to busitize.
      fb_tags - An array of facebook tags of faces you know to exist in the photo.
      fb_ignore_tag - The location of a face that we need to avoid busitizing.
      busey_count - How much Busey can you handle?
    """
    
    # Download the photo:
    response = requests.get(image_url)
    image_data = response.content
    
    file_name = os.path.basename(urlparse.urlparse(image_url).path)
    image_path = os.path.join(settings.MEDIA_ROOT, 'originals', file_name)
    image_file = open(image_path, 'wr')
    image_file.write(image_data)
    image_file.close()
    
    # Load it up in OpenCV (should maybe just keep it in memory?)
    cv_image = cv.LoadImage(image_path, 0)
    
    # The facebook tags are specified as percentages, let's convert those to pixels.
    tags = []
    for tag in fb_tags:
        print(tag)
        x = (tag['x']/100) * cv_image.width
        y = (tag['y']/100) * cv_image.height
        tags.append([x,y])
    
    # A list of the faces we've found in the image. So far, none.
    faces = []
    
    eye_frames = cv.HaarDetectObjects(cv_image, EYE_HC, cv.CreateMemStorage())
    for face_frame,n in cv.HaarDetectObjects(cv_image, FACE_HC, cv.CreateMemStorage()):
        face = Feature(face_frame)
        
        # If the face should be ignored, let's bail now.
        if fb_ignore_tag and face.contains_point(fb_ignore_tag[0], fb_ignore_tag[1]):
            continue
        
        if tags:
            face_valid = False
            for x,y in tags:
                if face.contains_point(x,y):
                    # If we found a face, and there's a tag there, it must be valid.
                    face_valid = True
                    break
            if face_valid:
                faces.append(face)

        """
        If the face hasn't been validated by facebook tags, we'll check for eyes in
        it. This drastically improves the reliability of the algorithm.
        """
        eyes_in_head = []
        for eye_frame,i in eye_frames:
            eye = Feature(eye_frame)
            if face.contains(eye):
                eyes_in_head.append(eye)
        
        # Given the set of eyes we found in this face, should it be considered valid?
        if eyes_valid(eyes_in_head):
            faces.append(face)
        
        # Have we had enough busey yet? CAN THERE BE TOO MUCH?
        if len(faces) == busey_count:
            break
    
    # If we didn't find any faces, let's get out now, while we still can.
    if len(faces) == 0:
        return None
    
    # Now we do the busitization
    original = Image.open(image_path)
    busitized = busitize_image(original, faces)
    busitized_path = image_path.replace('/originals/', '/busitized/')
    busitized.save(busitized_path)
    
    photo = Photo.objects.create(   user=user, 
                                    original=image_path, 
                                    busitized=busitized_path, 
                                    fb_id=fb_id, 
                                    tweet_id=tweet_id)
    return photo
    