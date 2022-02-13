from typing import Tuple
from PIL import ImageGrab, ImageOps
from PIL.Image import Image
from pytesseract import pytesseract


def grab_image(first_click: Tuple[int, int], last_click: Tuple[int, int]) -> Image:
    box = [0, 0, 0, 0]
    if first_click[0] < last_click[0]:
        box[0] = first_click[0]
        box[2] = last_click[0]
    else:
        box[2] = first_click[0]
        box[0] = last_click[0]

    if first_click[1] < last_click[1]:
        box[1] = first_click[1]
        box[3] = last_click[1]
    else:
        box[3] = first_click[1]
        box[1] = last_click[1]

    im = ImageGrab.grab(bbox=box)
    return im


def image_filter(image: Image) -> Image:
    # todo add filter to improve accuracy
    return ImageOps.grayscale(image)


def image_to_string(image: Image) -> str:
    content = pytesseract.image_to_string(image, lang="eng")
    return content
