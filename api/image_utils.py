from io import BytesIO
from typing import Union
from PIL import Image


class ImageUtils:
    def __init__(self):
        pass

    @staticmethod
    def resize(image: Image.Image, width: Union[int, None], height: Union[int, None]) -> Image.Image:
        if not width and not height:
            return image # nothing to do
        
        if not width and height:
            width = height
        elif width and not height:
            height = width
        
        copied_image = image.copy()
        copied_image.thumbnail((width, height))
        copied_image.format = image.format

        return copied_image

    @staticmethod
    def convert_to_unified_format(image: Image.Image) -> Image.Image:
        """
        Generates a new image from an input image with the following properties:
        - RGB color palette (no alpha channel)
        - PNG format
        - Maximum size: 2048 x 2048
        - no EXIF data from the input image

        Args:
            image (PIL.Image.Image): the image to convert

        Returns:
            PIL.Image.Image: the converted image
        """
        buf = BytesIO()
        rgb_image = image.convert("RGB")

        max_size = 2048

        if rgb_image.width > max_size or rgb_image.height > max_size:
            rgb_image.thumbnail((max_size, max_size))

        rgb_image.save(buf, format="png")
        buf.seek(0)
        new_image = Image.open(buf)
        return new_image
