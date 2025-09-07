import io
from typing import Union
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from api.cache import Cache
from api.classes import CachedImage
from api.image_utils import ImageUtils

app = FastAPI()
cache = Cache("assets/images")

def return_and_resize_image(image_id: str, image: CachedImage, width: Union[int, None] = None, height: Union[int, None] = None, download: bool = False) -> StreamingResponse:
    img_data = ImageUtils.resize(image.data, width, height)
    
    buf = io.BytesIO()
    img_data.save(fp=buf, format=img_data.format)
    buf.seek(0)
    
    content_disposition = "inline"
    if download:
        content_disposition = f'attachment; filename="{image_id}_{img_data.width}x{img_data.height}.{img_data.format.lower()}"'
    
    return StreamingResponse(buf, media_type=image.media_type, headers={'Content-Disposition': content_disposition, 'X-Image-Id': f'{image_id}'})

@app.get("/img/{image_id}")
async def get_image(image_id: str, width: Union[int, None] = None, height: Union[int, None] = None, download: bool = False):
    image = cache.get(image_id)    
    return return_and_resize_image(image_id, image, width, height, download)

@app.get("/img")
async def get_rand_image(width: Union[int, None] = None, height: Union[int, None] = None, download: bool = False):
    image_id, image = cache.get_random()    
    return return_and_resize_image(image_id, image, width, height, download)
