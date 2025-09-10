from dataclasses import dataclass
from typing import Union
from fastapi.responses import Response
import io
from PIL import Image

from .image_utils import ImageUtils


@dataclass
class CachedImage:
    data: Image.Image
    
    @property
    def width(self) -> int:
        return self.data.width

    @property
    def height(self) -> int:
        return self.data.height
    
    @property
    def media_type(self) -> str:
        return Image.MIME.get(self.data.format.upper())
    
    @property
    def id(self) -> str:
        return ImageUtils.get_id(data=self.data)
    
    def get_bytesio(self) -> io.BytesIO:
        buf = io.BytesIO()
        self.data.save(fp=buf, format=self.data.format)
        buf.seek(0)
        return buf


@dataclass
class ImageMetadata:
    original_width: int
    original_height: int
    media_type: str
    format: str
    
    def get_filename(self, id: str, scaled_width: Union[int, None], scaled_height: Union[int, None]) -> str:
        width = self.original_width if not scaled_width else scaled_width
        height = self.original_height if not scaled_height else scaled_height
        
        return ImageUtils.get_filename(id=id, width=width, height=height, format=self.format)
    
    @staticmethod
    def from_image(image: Image.Image) -> "ImageMetadata":
        return ImageMetadata(original_width=image.width, original_height=image.height, media_type=Image.MIME.get(image.format.upper()), format=image.format)

class FaviconResponse(Response):
    media_type = "image/svg+xml"
    