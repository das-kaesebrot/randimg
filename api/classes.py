import base64
from dataclasses import dataclass
import hashlib
import io
from PIL import Image


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
        pixel_bytes = self.data.tobytes()
        hash_input = f"{self.width}_{self.height}".encode("utf-8") + pixel_bytes
        digest = hashlib.sha256(hash_input).digest()
        return base64.urlsafe_b64encode(digest).decode("ascii")
    
    def get_bytesio(self) -> io.BytesIO:
        buf = io.BytesIO()
        self.data.save(fp=buf, format=self.data.format)
        buf.seek(0)
        return buf
    