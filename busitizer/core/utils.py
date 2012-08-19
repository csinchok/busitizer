import random
import os
from PIL import Image

from django.conf import settings

"""
Just some code that is useful in the busitization proccess. Didn't like
all of this being in the tasks.py
"""

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
        

def eyes_valid(eyes):
    """
    This method encasulates the logic to determine if a face is 'valid' given
    a set of eyes.
    """
    if len(eyes) in [1,2]:
        return True
    else:
        return False

    # TODO: figure out if we need to below to make things strict enough.
    if len(eyes) == 0:
        # No eyes? sketchy.
        return False
    
    if len(eyes) == 1:
        # Eh, one eye might be good enough.
        return True
    
    if len(eyes) > 2:
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
    
BUSEYS = [Image.open(os.path.join(settings.BUSEYS, filename)) 
                for filename in os.listdir(settings.BUSEYS)]

def busitize_image(image, faces):
    """
    Does Busitization on a PIL Image for the given faces
    """
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
            image.paste(overlay, paste_coord, mask=overlay)
        else:
            image.paste(overlay, paste_coord)
    return image