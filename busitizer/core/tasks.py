import os
import celery
import random
try:
    from cv2 import cv
except:
    print("You don't have OpenCV, so you won't be able to busitize :-(")
from PIL import Image

from django.conf import settings

FACE_HC = cv.Load(os.path.join(settings.HAAR_CASCADES, "haarcascade_frontalface_default.xml"))
EYE_HC = cv.Load(os.path.join(settings.HAAR_CASCADES, "haarcascade_eye.xml"))
BUSEYS = [Image.open(os.path.join(settings.BUSEYS, filename)) 
                for filename in os.listdir(settings.BUSEYS)]

class Feature(object):
    """
    This object just wraps an OpenCV frame, adding some useful methods.
    """
    def __init__(self, frame):
        self.x = frame[0]
        self.y = frame[1]
        self.width = frame[2]
        self.height = frame[3]
    
    def contains(self, feature):
        if feature.x < self.x:
            return False
        if feature.y < self.y:
            return False
        if (feature.x + feature.width) > (self.x + self.width):
            return False
        if (feature.y + feature.height) > (self.y + self.height):
            return False
        return True

    def contains_point(self, x, y):
        if x < self.x:
            return False
        if x > (self.x + self.width):
            return False
        if y < self.y:
            return False
        if y > (self.y + self.height):
            return False
        return True

    def overlaps_x(self, feature):
        return (feature.x >= self.x) and (feature.x <= (self.x + self.width))

    def overlaps_y(self, feature):
        return (feature.y >= self.y) and (feature.y <= (self.y + self.height))

    def overlaps(self, feature):
        return (self.overlaps_x(feature) and self.overlaps_y(feature))

def _face_valid(face, eyes):
    """
    This method encasulates the logic to determine if a face is 'valid' given
    a set of eyes.
    """
    if len(eyes) != 2:
        # If we dont' have two eyes, it's not valid.
        return False
    
    # If the eyes overlap eachother on the x axis, the face is probably not valid.
    if eyes[0].overlaps_x(eyes[1]):
        return False
    if eyes[1].overlaps_x(eyes[0]):
        return False
        
    # We make sure that the eyes overlap eachother on the y axis.
    if (not eyes[0].overlaps_y(eyes[1])) and (not eyes[1].overlaps_y(eyes[0])):
        return False
    return True

@celery.task
def busitize(image_path, tags=[], ignore=[], busey_count=5):
    """
    This task determines if an image is 'bustizable', and if so, busitizes it,
    returning the path of the busitized image. The algorithm is pretty strict,
    since we'd like to avoid incorrectly busitizing anything.
    
    Here's how the params work:
      image_path - Required, the absolute path to the image you would like to busitize.
      tags - An array of [x,y] locations to faces you know to exist in the photo.
      ignore - The [x,y] location of a face that we need to avoid busitizing.
      busey_count - How much Busey can you handle?
    """
    
    cv_image = cv.LoadImage(image_path, 0)
    
    # A list of the faces we've found in the image. So far, none.
    faces = []
    
    eye_frames = cv.HaarDetectObjects(cv_image, EYE_HC, cv.CreateMemStorage())
    for face_frame,n in cv.HaarDetectObjects(cv_image, FACE_HC, cv.CreateMemStorage()):
        face = Feature(face_frame)
        
        # If the face should be ignored, let's bail now.
        if face.contains_point(ignore[0], ignore[1]):
            continue
        
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
        if _face_valid(face, eyes_in_head):
            faces.append(face)
        
        # Have we had enough busey yet? CAN THERE BE TOO MUCH?
        if len(faces) == busey_count:
            break
    
    # If we didn't find any faces, let's get out now, while we still can.
    if len(faces) == 0:
        return None
    
    # Now we do the busitization
    original = Image.open(image_path)
    for face in faces:
        # Make the overlay a little larger than the feature, because it's funnier.
        overlay = random.choice(BUSEYS).resize((int(face.width * 1.4), int(face.height * 1.4)))
        # Twist it a little
        overlay = overlay.rotate(random.randint(-15,15))
        # Maybe flip it horizontally
        if random.random() < 0.5:
            overlay = overlay.transpose(Image.FLIP_LEFT_RIGHT)
            
        # If the mode is RGBA, we use the mask, otherwise
        paste_coord = (face.x - (face.width/6), face.y - (face.height/3))
        if overlay.mode == 'RGBA':
            original.paste(overlay, paste_coord, mask=overlay)
        else:
            original.paste(overlay, paste_coord)
    
    busitized_path = "%s_busitized%s" % os.path.splitext(image_path)
    original.save(busitized_path)
        
    return busitized_path
    