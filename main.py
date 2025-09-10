import os
from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.cache import Cache
from api.classes import FaviconResponse, ImageMetadata

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

ENV_PREFIX = "RANDIMG"

source_image_dir = os.getenv(f"{ENV_PREFIX}_IMAGE_DIR", "assets/images")
cache_dir = os.getenv(f"{ENV_PREFIX}_CACHE_DIR", "cache")

cache = Cache(image_dir=source_image_dir, cache_dir=cache_dir)

def return_file(image_id: str, filename: str, metadata: ImageMetadata, download: bool = False) -> FileResponse:
    content_disposition = "inline"
    if download:
        content_disposition = f'attachment; filename="{filename}"'
        
    return FileResponse(path=filename, media_type=metadata.media_type, headers={'Content-Disposition': content_disposition, 'X-Image-Id': f'{image_id}', "Cache-Control": "max-age=2592000, public, no-transform"})

@app.get("/favicon.ico", response_class=FaviconResponse)
async def get_favicon():
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        + '<text y=".9em" font-size="90">🦈</text>'
        + "</svg>"
    )

@app.get("/", response_class=Union[HTMLResponse, RedirectResponse])
async def page_redirect_rand_image(request: Request, redirect: bool = False):
    image_id = cache.get_random_id()
    
    if redirect:
        return RedirectResponse(image_id)
    
    filename = cache.get_filename_and_generate_copy_if_missing(image_id)
    return templates.TemplateResponse(request=request, name="image.html", context={"image_id": image_id, "image_filename": filename, "height": 512})

@app.get("/{image_id}", response_class=HTMLResponse)
async def page_get_image(request: Request, image_id: str):
    filename = cache.get_filename_and_generate_copy_if_missing(image_id)
    return templates.TemplateResponse(request=request, name="image.html", context={"image_id": image_id, "image_filename": filename, "height": 512})

@app.get("/api/img/{image_id}")
async def api_get_image(image_id: str, width: Union[int, None] = None, height: Union[int, None] = None, download: bool = False):
    filename = cache.get_filename_and_generate_copy_if_missing(image_id, width=width, height=height)
    metadata = cache.get_metadata(image_id)
    return return_file(image_id, filename, metadata, download)

@app.get("/api/img")
async def api_get_rand_image(width: Union[int, None] = None, height: Union[int, None] = None, download: bool = False):
    image_id = cache.get_random_id()
    filename = cache.get_filename_and_generate_copy_if_missing(image_id, width=width, height=height)
    metadata = cache.get_metadata(image_id)
    return return_file(image_id, filename, metadata, download)
