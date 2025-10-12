
import os
from PIL import Image, ImageOps

def load_image(filepath, max_width=None, scale_factor=1):
    image = Image.open(filepath)
    if not max_width:
        max_width = image.size[0]
    max_width = int(max_width * scale_factor)
    w_percent = (max_width / float(image.size[0]))
    h_size = int((float(image.size[1]) * float(w_percent)))
    image = image.resize((max_width, h_size))


    return image


from PIL import Image
import os

def prepare_escpos_image(image):
    """
    Prepares an image for ESC/POS printing:
      - Flattens transparent images to white background
      - Converts to grayscale
      - Scales by width or factor
      - Converts to pure black & white (1-bit)


    Returns:
        PIL.Image.Image: A ready-to-print 1-bit monochrome image.
    """
    

    # --- Handle transparency ---
    if image.mode == "RGBA":
        bg = Image.new("RGBA", image.size, (255, 255, 255, 255))
        bg.paste(image, mask=image.split()[3])  # use alpha as mask
        image = bg.convert("L")  # grayscale
    elif image.mode != "L":
        image = image.convert("L")

     # --- Apply automatic contrast stretch (optional but helps) ---
    image = ImageOps.autocontrast(image)

    # --- Convert to 1-bit with dithering ---
    image_bw = image.convert("1")  # uses Floyd–Steinberg dithering

    return image_bw