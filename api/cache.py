import os
from PIL import Image
from typing import Dict, Union
from .classes import CachedImage
from .image_utils import ImageUtils

class Cache:
    img_dict: Dict[str, CachedImage] = {}

    def __init__(self, image_dir: str):
        self.img_dict = Cache._generate_cache(image_dir)
        
    
    @staticmethod
    def _generate_cache(image_dir: str) -> Dict[str, CachedImage]:
        images: list[Image.Image] = []
        
        for filename in os.listdir(image_dir):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                img = Image.open(filename)
                img.load()
                images.append(img)
                
        image_dict = {}
                
        for image in images:
            image = ImageUtils.convert_to_unified_format(image)
            cached_image = CachedImage(data=image)
            image_dict[cached_image.id] = cached_image
            
        return image_dict

    def get(self, id: str) -> Union[CachedImage, None]:
        return self.img_dict.get(id)
    