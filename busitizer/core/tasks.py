import os
import celery
import random
from cv2 import cv
from PIL import Image, ImageOps, ImageFilter, ImageDraw

from django.conf import settings

FACE_HC = cv.Load(os.path.join(settings.HAAR_CASCADES, "haarcascade_frontalface_default.xml"))
BUSEYS = [Image.open(os.path.join(settings.BUSEYS, filename)) for filename in os.listdir(settings.BUSEYS)]

class Feature(object):
    
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
        return (x > self.x) and (x < (self.x + self.width)) and (y > self.y) and (y < (self.y + self.height))

    def overlaps_x(self, feature):
        return (feature.x >= self.x) and (feature.x <= (self.x + self.width))

    def overlaps_y(self, feature):
        return (feature.y >= self.y) and (feature.y <= (self.y + self.height))

    def overlaps(self, feature):
        return (self.overlaps_x(feature) and self.overlaps_y(feature))

@celery.task
def busitize(image_path, faces=[], busey_count=1):
    cv_image = cv.LoadImage(image_path, 0)
    
    features = []
    for frame,n in cv.HaarDetectObjects(cv_image, FACE_HC, cv.CreateMemStorage()):
        feature = Feature(frame)
        
        # TODO: get face locations from fb, fall back to eye detection
        features.append(feature)
        
        #for x,y in faces:
        #    if feature.contains_point(x,y):
        #        features.append(feature)
        #        break
        if len(features) == busey_count:
            break
    
    if len(features) == 0:
        return None
    
    original = Image.open(image_path)
    for feature in features:
        # Make the overlay a little larger than the feature, because it's funnier.
        overlay = random.choice(BUSEYS).resize((int(feature.width * 1.4), int(feature.height * 1.4)))
        # Twist it a little
        overlay = overlay.rotate(random.randint(-15,15))
        # Maybe flip it horizontally
        if random.random() < 0.5:
            overlay = overlay.transpose(Image.FLIP_LEFT_RIGHT)
        if overlay.mode == 'RGBA':
            original.paste(overlay, (feature.x - (feature.width/6), feature.y - (feature.height/3)), mask=overlay)
        else:
            original.paste(overlay, (feature.x - (feature.width/6), feature.y - (feature.height/3)))
    
    busitized_path = "%s_busitized%s" % os.path.splitext(image_path)
    original.save(busitized_path)
        
    return busitized_path
    