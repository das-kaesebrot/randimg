import base64
import hashlib
from io import BytesIO
import os
from typing import Union
from PIL import Image

from .classes import ImageMetadata

MAX_SIZE = 2048
FORMAT = "png"

class ImageUtils:
    def __init__(self):
        pass

    @staticmethod
    def resize(image: Image.Image, width: Union[int, None] = None, height: Union[int, None] = None, copy: bool = True) -> Image.Image:
        if not width and not height:
            return image # nothing to do
        
        if not width and height:
            width = height
        elif width and not height:
            height = width
        
        new_image = image
        
        if copy:
            new_image = image.copy()
            
        new_image.thumbnail((width, height))
        new_image.format = image.format

        return new_image

    @staticmethod
    def convert_to_unified_format_in_buffer(image: Image.Image) -> Image.Image:
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
        rgb_image = image.convert("RGB")

        max_size = MAX_SIZE

        if rgb_image.width > max_size or rgb_image.height > max_size:
            rgb_image = ImageUtils.resize(rgb_image, max_size, max_size, copy=False)

        buf = BytesIO()
        rgb_image.save(buf, format=FORMAT)
        buf.seek(0)
        new_image = Image.open(buf)
        return new_image

    @staticmethod
    def convert_to_unified_format_and_write_to_filesystem(output_path: str, image: Image.Image) -> tuple[str, ImageMetadata]:
        """
        Generates a new image from an input image with the following properties:
        - RGB color palette (no alpha channel)
        - PNG format
        - Maximum size: 2048 x 2048
        - no EXIF data from the input image

        Args:
            output_path (str): the path to write the image to (filename will be appended)
            image (PIL.Image.Image): the image to convert
        """
        
        rgb_image = image.convert("RGB")

        max_size = MAX_SIZE

        if rgb_image.width > max_size or rgb_image.height > max_size:
            rgb_image = ImageUtils.resize(rgb_image, max_size, max_size, copy=False)
                
        os.makedirs(output_path, exist_ok=True)
        
        id = ImageUtils.get_id(rgb_image)        
        filename = os.path.join(output_path, ImageUtils.get_filename(id=id, width=rgb_image.width, height=rgb_image.height, format=FORMAT))
        rgb_image.save(filename, format=FORMAT)
        
        metadata = ImageMetadata(original_width=rgb_image.width, original_height=rgb_image.height, media_type=Image.MIME.get(FORMAT.upper()), format=FORMAT)
        
        return (id, metadata)
    
    @staticmethod
    def write_scaled_copy_from_source_filename_to_filesystem(*, id: str, source_filename: str, output_path: str, width: Union[int, None] = None, height: Union[int, None] = None):
        source = Image.open(source_filename)
        ImageUtils.write_scaled_copy_to_filesystem(source=source, output_path=output_path, width=width, height=height)
        
    @staticmethod
    def write_scaled_copy_to_filesystem(*, id: str, source: Image.Image,  output_path: str, width: Union[int, None] = None, height: Union[int, None] = None):
        image = ImageUtils.resize(source, width, height, copy=False)
        filename = os.path.join(output_path, ImageUtils.get_filename_with_image_data(id=id, data=image))
        image.save(filename)
    
    @staticmethod
    def get_filename_with_image_data(*, id: str, data: Image.Image):
        return ImageUtils.get_filename(id=id, width=data.width, height=data.height, format=data.format)
    
    @staticmethod
    def get_filename(*, id: str, width: int, height: int, format: str):
        return f"{id}_{width}x{height}.{format.lower()}"
    
    @staticmethod
    def get_id(*, data: Image.Image) -> str:
        pixel_bytes = data.tobytes()
        hash_input = f"{data.width}_{data.height}".encode("utf-8") + pixel_bytes
        digest = hashlib.sha256(hash_input).digest()
        return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")