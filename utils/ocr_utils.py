from io import BytesIO
from pathlib import Path

import easyocr
import numpy as np
from PIL import Image

reader = easyocr.Reader(['en'], gpu=False)


def ocr_image(image_source) -> str:
    """Extract text from a PIL image, file path, numpy array, or raw bytes.

    EasyOCR expects either a file path (string), bytes, or a numpy array. This
    helper normalizes PIL.Image inputs into numpy arrays before calling EasyOCR.
    """

    # Load from bytes or path
    if isinstance(image_source, (bytes, bytearray)):
        image = Image.open(BytesIO(image_source))
    elif isinstance(image_source, (str, Path)):
        image = Image.open(image_source)
    else:
        image = image_source

    # If it's a PIL image, convert to RGB numpy array for EasyOCR
    if isinstance(image, Image.Image):
        image = image.convert('RGB')
        img_np = np.array(image)
    elif isinstance(image, np.ndarray):
        img_np = image
    else:
        raise TypeError('Invalid input type. Supporting format = string(file path or url), bytes, numpy array, or PIL.Image')

    result = reader.readtext(img_np)
    lines = [item[1].strip() for item in result if item[1].strip()]
    return '\n'.join(lines)
