import logging
import os
import random
from threading import Thread
import inotify.adapters
import inotify.constants
from PIL import Image
from typing import Dict, Union
from .classes import ImageMetadata
from .filename_utils import FilenameUtils
from .image_utils import ImageUtils
from .utils import Utils

from datetime import timedelta
from time import perf_counter


class Cache:
    _ids_to_metadata: Dict[str, ImageMetadata] = {}
    _image_dir: str
    _cache_dir: str
    _logger: logging.Logger
    
    _inotify_thread: Thread

    def __init__(self, *, image_dir: str, cache_dir: str, enable_inotify: bool = True):
        image_dir = os.path.abspath(image_dir)
        cache_dir = os.path.abspath(cache_dir)
        
        self._logger = logging.getLogger(__name__)
        self._logger.info(f"Created cache instance with image directory='{image_dir}' and cache directory='{cache_dir}'")
        self._cache_dir = cache_dir
        self._image_dir = image_dir
        self._generate_cache()
        
        if enable_inotify: self._dispatch_inotify_thread()

    def _generate_cache(self) -> Dict[str, ImageMetadata]:
        start = perf_counter()
        image_dir = self._image_dir
        
        images: list[Image.Image] = []

        for filename in os.listdir(image_dir):
            if (
                filename.lower().endswith(".jpg")
                or filename.lower().endswith(".jpeg")
                or filename.lower().endswith(".png")
            ):
                try:
                    img = Image.open(os.path.join(image_dir, filename))
                    img.load()
                    images.append(img)
                except OSError as e:
                    self._logger.exception(f"Failed loading file '{os.path.join(image_dir, filename)}'")
                    continue

        metadata_dict = {}

        for image in images:
            try:
                id, metadata = ImageUtils.convert_to_unified_format_and_write_to_filesystem(
                    output_path=self._cache_dir, image=image
                )
                metadata_dict[id] = metadata
            except OSError:
                self._logger.exception(f"Failed writing converted file '{'no filename' if not image.filename else image.filename}'")
                continue

        self._ids_to_metadata = metadata_dict    
        end = perf_counter()
        self._logger.info(f"Generated {len(self._ids_to_metadata.keys())} cached images in {timedelta(seconds=end-start)}")
    
    def _dispatch_inotify_thread(self):
        self._logger.info("Starting inotify thread")
        
        self._inotify_thread = Thread(target=self._watch_fs_events)
        self._inotify_thread.start()
    
    def _watch_fs_events(self):
        try:            
            i = inotify.adapters.Inotify()

            i.add_watch(self._image_dir, mask=inotify.constants.IN_DELETE | inotify.constants.IN_CLOSE_WRITE)

            for event in i.event_gen(yield_nones=False):
                (_, type_names, path, filename) = event
                self._logger.debug(event)
                
        except KeyboardInterrupt or InterruptedError as e:
            self._logger.info(f"{type(e).__name__} received. Stopping thread.")

    def get_filename_and_generate_copy_if_missing(
        self, id: str, width: Union[int, None] = None, height: Union[int, None] = None, crop: bool = False
    ) -> str:
        metadata = self._ids_to_metadata.get(id)

        width, height = Utils.clamp(width, 0, metadata.original_width), Utils.clamp(
            height, 0, metadata.original_height
        )
        
        if not crop:
            width, height = ImageUtils.calculate_scaled_size(
                metadata.original_width,
                metadata.original_height,
                width=width,
                height=height,
            )

        filename = os.path.join(
            self._cache_dir,
            FilenameUtils.get_filename(
                id=id, width=width, height=height, format=metadata.format
            ),
        )

        if not os.path.isfile(filename):
            source_filename = os.path.join(
                self._cache_dir,
                FilenameUtils.get_filename(
                    id=id,
                    width=metadata.original_width,
                    height=metadata.original_height,
                    format=metadata.format,
                ),
            )
            filename = ImageUtils.write_scaled_copy_from_source_filename_to_filesystem(
                id=id,
                source_filename=source_filename,
                output_path=self._cache_dir,
                width=width,
                height=height,
                crop=crop,
            )

        return filename

    def get_random_id(self) -> str:
        return random.choice(list(self._ids_to_metadata.keys()))

    def get_random(self) -> tuple[str, ImageMetadata]:
        return random.choice(list(self._ids_to_metadata.values()))

    def get_metadata(self, id: str) -> Union[ImageMetadata, None]:
        return self._ids_to_metadata.get(id)
    
    def id_exists(self, id: str) -> bool:
        return id in self._ids_to_metadata.keys()
    
    def get_first_id(self) -> dict[str, ImageMetadata]:
        return sorted(self._ids_to_metadata.keys())[0]
