import io
from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL.Image import Image

from api.cache import Cache
from api.classes import CachedImage, FaviconResponse
from api.image_utils import ImageUtils

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

cache = Cache("assets/images")

def get_filename(image_id: str, image_data: Image):
    return f"{image_id}_{image_data.width}x{image_data.height}.{image_data.format.lower()}"

def return_and_resize_image(image_id: str, image: CachedImage, width: Union[int, None] = None, height: Union[int, None] = None, download: bool = False) -> StreamingResponse:
    img_data = ImageUtils.resize(image.data, width, height)
    
    buf = io.BytesIO()
    img_data.save(fp=buf, format=img_data.format)
    buf.seek(0)
    
    content_disposition = "inline"
    if download:
        content_disposition = f'attachment; filename="{get_filename(image_id, img_data)}"'
    
    return StreamingResponse(buf, media_type=image.media_type, headers={'Content-Disposition': content_disposition, 'X-Image-Id': f'{image_id}', "Cache-Control": "max-age=2592000, public, no-transform"})

@app.get("/favicon.ico", response_class=FaviconResponse)
async def get_favicon():
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        + '<text y=".9em" font-size="90">🦈</text>'
        + "</svg>"
    )

@app.get("/", response_class=RedirectResponse)
async def page_redirect_rand_image(request: Request):
    return cache.get_random_id()

@app.get("/{image_id}", response_class=HTMLResponse)
async def page_get_image(request: Request, image_id: str):
    image = cache.get(image_id)
    filename = get_filename(image_id=image_id, image_data=image.data)
    return templates.TemplateResponse(request=request, name="image.html", context={"image_id": image_id, "image_filename": filename, "height": 512})

@app.get("/api/img/{image_id}")
async def api_get_image(image_id: str, width: Union[int, None] = None, height: Union[int, None] = None, download: bool = False):
    image = cache.get(image_id)    
    return return_and_resize_image(image_id, image, width, height, download)

@app.get("/api/img")
async def api_get_rand_image(width: Union[int, None] = None, height: Union[int, None] = None, download: bool = False):
    image_id, image = cache.get_random()    
    return return_and_resize_image(image_id, image, width, height, download)
