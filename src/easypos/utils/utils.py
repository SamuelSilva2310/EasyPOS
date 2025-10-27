
import os
from PIL import Image, ImageOps
from easypos.settings import APP_SETTINGS
from pathlib import Path
import sys


def resource_path(relative_path: str) -> str:
    """Get absolute path to resource for dev and PyInstaller builds"""

    #relative_path = Path(relative_path)
    return Path(os.path.join(APP_SETTINGS.RUNTIME_DIRECTORY, relative_path))
        

def load_image(filepath, max_width=None, scale_factor=1):
    image = Image.open(resource_path(filepath))
    if not max_width:
        max_width = image.size[0]
    max_width = int(max_width * scale_factor)
    w_percent = (max_width / float(image.size[0]))
    h_size = int((float(image.size[1]) * float(w_percent)))
    image = image.resize((max_width, h_size))


    return image




def prepare_escpos_image(image, target_width=None, max_height=None):
    """
    Prepares an image for ESC/POS thermal printing.

    Steps:
      - Flattens transparency to white background
      - Converts to grayscale
      - Optionally rescales by target width (preserving aspect ratio)
      - Applies auto-contrast
      - Converts to 1-bit dithered black & white

    Args:
        image (PIL.Image.Image): Input image.
        target_width (int, optional): Resize width in pixels. Keeps aspect ratio.
        max_height (int, optional): Limit max height after scaling.

    Returns:
        PIL.Image.Image: Ready-to-print 1-bit monochrome image.
    """

    # --- Handle transparency ---
    if image.mode == "RGBA":
        bg = Image.new("RGBA", image.size, (255, 255, 255, 255))
        bg.paste(image, mask=image.split()[3])  # use alpha as mask
        image = bg.convert("L")  # grayscale
    elif image.mode != "L":
        image = image.convert("L")

    # --- Optional resize ---
    if target_width:
        aspect_ratio = image.height / image.width
        new_height = int(target_width * aspect_ratio)
        if max_height and new_height > max_height:
            new_height = max_height
            target_width = int(max_height / aspect_ratio)
        image = image.resize((target_width, new_height), Image.LANCZOS)

    # --- Improve contrast ---
    image = ImageOps.autocontrast(image)

    # --- Convert to 1-bit with Floyd–Steinberg dithering ---
    image_bw = image.convert("1")

    return image_bw