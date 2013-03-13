import os
from celery import task
import random
import requests
import urlparse
import json
import hashlib

from django.conf import settings
from django.core.cache import cache
from django.core.files import File

from PIL import Image as PILImage

from busitizer.core.models import Image
from busitizer.core.utils import Feature, eyes_valid, busitize_image

from cv2 import cv
FACE_HC = cv.Load(os.path.join(settings.HAAR_CASCADES, "haarcascade_frontalface_alt.xml"))
EYE_HC = cv.Load(os.path.join(settings.HAAR_CASCADES, "haarcascade_eye.xml"))

def on_failure(self, exc, task_id, args, kwargs, einfo):
    image = Image.objects.get(id=args[0])
    image.status = Image.FAILED
    image.save()

@task
def busitize(image_id, busey_count=5):

    image = Image.objects.get(id=image_id)

    url = image.url
    # Each URL should be saved to the same location each time.
    file_path, file_extension = os.path.splitext(urlparse.urlparse(url).path)
    file_name = "%s%s" % (hashlib.sha1(file_path).hexdigest(), file_extension)
    image_path = os.path.join(settings.MEDIA_ROOT, 'originals', file_name)

    response = requests.get(url)
    image_data = response.content
    image_file = open(image_path, 'wr')
    image_file.write(image_data)
    image_file.close()

    # Load it up in OpenCV (should maybe just keep it in memory?)
    cv_image = cv.LoadImage(image_path, 0)

    # A list of the faces we've found in the image. So far, none.
    faces = []

    eye_frames = cv.HaarDetectObjects(cv_image, EYE_HC, cv.CreateMemStorage())
    for face_frame,n in cv.HaarDetectObjects(cv_image, FACE_HC, cv.CreateMemStorage()):
        face = Feature(face_frame)
        
        # If this face overlaps any over faces, let's bail now.
        for valid_face in faces:
            if face.overlaps(valid_face):
                print("face overlaps an existing face")
                continue

        faces.append(face)

        """
        We check for eyes in the face. This drastically improves the reliability of the algorithm.
        """
        eyes_in_head = []
        for eye_frame,i in eye_frames:
            eye = Feature(eye_frame)
            if face.contains(eye):
                eyes_in_head.append(eye)
                
        # Given the set of eyes we found in this face, should it be considered valid?
        # if eyes_valid(eyes_in_head):
        #     print("the eyes say yes")
        #     faces.append(face)
        # else:
        #     print("the eyes say no")
        
        # Have we had enough busey yet? CAN THERE BE TOO MUCH?
        if len(faces) == busey_count:
            break

    # If we didn't find any faces, let's get out now, while we still can.
    if len(faces) == 0:
        print("No faces....failed")
        image.status = Image.FAILED
        image.save()
        return None
    
    # Now we do the busitization
    original = PILImage.open(image_path)
    busitized = busitize_image(original, faces)

    os.remove(image_path)
    tmp = os.tmpfile()
    busitized.save(tmp, 'png')

    print("busitized!")
    image.busitized.save("%d.png" % image.id, File(tmp))
    image.status = Image.COMPLETED
    image.save()
    tmp.close()
    return image.busitized.url
