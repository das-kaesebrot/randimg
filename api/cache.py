import os
import random
from PIL import Image
from typing import Dict, Union
from .classes import ImageMetadata
from .filename_utils import FilenameUtils
from .image_utils import ImageUtils
from .utils import Utils

class Cache:
    _metadata_dict: Dict[str, ImageMetadata] = {}
    _cache_dir: str

    def __init__(self, *, image_dir: str, cache_dir: str):
        self._cache_dir = cache_dir
        self._generate_cache(image_dir)
        
    def _generate_cache(self, image_dir: str) -> Dict[str, ImageMetadata]:
        images: list[Image.Image] = []
        
        for filename in os.listdir(image_dir):
            if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
                img = Image.open(os.path.join(image_dir, filename))
                img.load()
                images.append(img)
                
        metadata_dict = {}
                
        for image in images:
            id, metadata = ImageUtils.convert_to_unified_format_and_write_to_filesystem(output_path=self._cache_dir, image=image)
            metadata_dict[id] = metadata
            
        self._metadata_dict = metadata_dict
    
    def get_filename_and_generate_copy_if_missing(self, id: str, width: Union[int, None] = None, height: Union[int, None] = None) -> str:
        metadata = self._metadata_dict.get(id)
        
        if not width:
            width = metadata.original_width
        
        if not height:
            height = metadata.original_height
            
        width, height = Utils.clamp(width, 0, metadata.original_width), Utils.clamp(height, 0, metadata.original_height)        
        width, height = ImageUtils.calculate_scaled_size(metadata.original_width, metadata.original_height, width=width, height=height)
                    
        filename = os.path.join(self._cache_dir, FilenameUtils.get_filename(id=id, width=width, height=height, format=metadata.format))
        
        if not os.path.isfile(filename):
            source_filename = os.path.join(self._cache_dir, FilenameUtils.get_filename(id=id, width=metadata.original_width, height=metadata.original_height, format=metadata.format))
            filename = ImageUtils.write_scaled_copy_from_source_filename_to_filesystem(id=id, source_filename=source_filename, output_path=self._cache_dir, width=width, height=height)
        
        return filename
    
    def get_random_id(self) -> str:
        return random.choice(list(self._metadata_dict.keys()))
    
    def get_random(self) -> tuple[str, ImageMetadata]:
        return random.choice(list(self._metadata_dict.values()))
    
    def get_metadata(self, id: str) -> Union[ImageMetadata, None]:
        return self._metadata_dict.get(id)
    