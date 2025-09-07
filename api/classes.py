import base64
from dataclasses import dataclass
import hashlib


@dataclass
class CachedImage:
    width: int
    height: int
    data: bytes
    media_type: str
    
    def get_id(self) -> str:
        hash = hashlib.sha256(self.data)
        return base64.urlsafe_b64encode(hash.digest())
    