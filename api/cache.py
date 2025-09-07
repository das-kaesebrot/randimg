from typing import Dict, Union
from .classes import CachedImage


class Cache:
    img_dict: Dict[str, CachedImage] = {}

    def __init__(self, image_path: str):
        pass
    
    @staticmethod
    def _generate_cache(image) -> Dict[str, CachedImage]:
        pass

    def get(self, id: str) -> Union[CachedImage, None]:
        return self.img_dict.get(id)
    