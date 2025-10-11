
import os
from PIL import Image

def load_image(filepath, max_width=None, scale_factor=1):
    image = Image.open(filepath)
    if not max_width:
        max_width = image.size[0]
    max_width = int(max_width * scale_factor)
    w_percent = (max_width / float(image.size[0]))
    h_size = int((float(image.size[1]) * float(w_percent)))
    image = image.resize((max_width, h_size))
    return image
