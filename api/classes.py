from dataclasses import dataclass
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
    

class FaviconResponse(Response):
    media_type = "image/svg+xml"